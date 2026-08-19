from __future__ import annotations

import argparse, ast, hashlib, json, os, platform, re, time
from pathlib import Path
import numpy as np
import torch
from huggingface_hub import model_info
from transformers import AutoModelForCausalLM, AutoTokenizer

ZERO=(); ONE=((0,0,1),); X=((1,0,1),); Y=((0,1,1),)
def fd(d): return tuple(sorted((i,j,int(c)) for (i,j),c in d.items() if int(c)))
def dd(p): return {(i,j):c for i,j,c in p}
def add(a,b):
 d=dd(a)
 for i,j,c in b:d[(i,j)]=d.get((i,j),0)+c
 return fd(d)
def neg(a): return tuple((i,j,-c) for i,j,c in a)
def sub(a,b): return add(a,neg(b))
def mul(a,b):
 d={}
 for ai,aj,ac in a:
  for bi,bj,bc in b:d[(ai+bi,aj+bj)]=d.get((ai+bi,aj+bj),0)+ac*bc
 return fd(d)
def power(a,n):
 r=ONE
 for _ in range(n):r=mul(r,a)
 return r
def val(p,x,y): return int(sum(c*x**i*y**j for i,j,c in p))
def ast_poly(n):
 if isinstance(n,ast.Expression):return ast_poly(n.body)
 if isinstance(n,ast.Name) and n.id in {'x','y'}:return X if n.id=='x' else Y
 if isinstance(n,ast.Constant) and isinstance(n.value,int):return ZERO if n.value==0 else ((0,0,int(n.value)),)
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return neg(ast_poly(n.operand))
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.UAdd):return ast_poly(n.operand)
 if isinstance(n,ast.BinOp):
  a,b=ast_poly(n.left),ast_poly(n.right)
  if isinstance(n.op,ast.Add):return add(a,b)
  if isinstance(n.op,ast.Sub):return sub(a,b)
  if isinstance(n.op,ast.Mult):return mul(a,b)
  if isinstance(n.op,ast.Pow) and isinstance(n.right,ast.Constant) and 0<=int(n.right.value)<=6:return power(a,int(n.right.value))
 raise ValueError(ast.dump(n))
def parse_expr(text):
 s=text.replace('²','**2').replace('^','**').replace('−','-').replace('×','*')
 s=re.sub(r'\bxy\b','x*y',s); cs=[]
 for m in re.finditer(r'(?:Expression|Answer|f\s*\(\s*x\s*,\s*y\s*\))\s*[:=]\s*([^\n`]+)',s,re.I):cs.append(m.group(1))
 cs+=re.findall(r'```(?:python)?\s*([^`]+)```',s,re.I|re.S);cs += [x for x in s.splitlines() if x.strip()]+[s]
 for c in reversed(cs):
  c=c.strip().strip('`$ .;,')
  if '=' in c:c=c.split('=')[-1].strip()
  c=re.sub(r'\b([0-9]+)\s*([xy])\b',r'\1*\2',c).split(' where ')[0].split(' because ')[0].strip()
  if not c or len(c)>300:continue
  try:return ast_poly(ast.parse(c,mode='eval'))
  except Exception:pass
 return None
def ev(rows):return '\n'.join(f"f({r['x']},{r['y']})={r['value']}" for r in rows)
DEMO='''Example 1
f(-1,-1)=-2
f(0,2)=2
f(2,1)=3
Expression: x + y

Example 2
f(-1,2)=-4
f(0,-1)=1
f(2,3)=3
Expression: x*y - y
'''
def free_prompt(rows):return 'Infer the exact integer polynomial from observations. Use only x, y, integer constants, +, -, and *. Return one expression.\n\n'+DEMO+'\nTarget\n'+ev(rows)+'\nExpression:'
def rank_prompt(rows):return 'Infer the integer polynomial f from the observations. The next text must be the exact expression for f.\n'+ev(rows)+'\nExpression:'
def teach_prompt(e):return f'The exact rule has been taught: f(x,y) = {e}.\nRepeat an algebraically equivalent rule using x and y.\nExpression:'
def query_prompt(r):
 hs='\n'.join(f"H{i+1}: {c['expression']}" for i,c in enumerate(r['query_choice']['candidates']))
 qs='\n'.join(f"{o['label']}: evaluate at ({o['x']},{o['y']})" for o in r['query_choice']['query_options'])
 return 'Choose one experiment that separates the candidate polynomial hypotheses as strongly as possible.\n'+hs+'\nQueries:\n'+qs+'\nAnswer:'
def transfer_prompt(e,x,y):return f"A reusable binary operator is M(a,b) = {e.replace('x','a').replace('y','b')}. Compute M(M({x},{y}),{y}). Write only the integer.\nAnswer:"
def generate(m,t,p,n):
 z=t(p,return_tensors='pt')
 with torch.inference_mode():o=m.generate(**z,max_new_tokens=n,do_sample=False,pad_token_id=t.eos_token_id,eos_token_id=t.eos_token_id,use_cache=True)
 return t.decode(o[0,z['input_ids'].shape[1]:],skip_special_tokens=True)
def scores(m,t,p,cs):
 pi=t(p,add_special_tokens=True)['input_ids'];seq=[];pls=[]
 for c in cs:
  ci=t(' '+c,add_special_tokens=False)['input_ids'];seq.append(pi+ci);pls.append(len(pi))
 ml=max(map(len,seq));pad=t.pad_token_id if t.pad_token_id is not None else t.eos_token_id
 ids=torch.full((len(seq),ml),pad,dtype=torch.long);att=torch.zeros_like(ids)
 for i,s in enumerate(seq):ids[i,:len(s)]=torch.tensor(s);att[i,:len(s)]=1
 with torch.inference_mode():lp=torch.log_softmax(m(input_ids=ids,attention_mask=att).logits[:,:-1,:],dim=-1)
 out=[]
 for i,s in enumerate(seq):
  lab=ids[i,pls[i]:len(s)];pos=torch.arange(pls[i]-1,len(s)-1);v=lp[i,pos,lab]
  out.append({'continuation':cs[i],'sum_logprob':float(v.sum()),'mean_logprob':float(v.mean()),'tokens':int(v.numel())})
 return out
def rank(sc,ci):return sorted(range(len(sc)),key=lambda i:(-sc[i]['mean_logprob'],i)).index(ci)+1
def numeric_options(correct,decoys):
 vs=[correct]
 for x in decoys:
  if x not in vs:vs.append(x)
  if len(vs)==8:break
 d=1
 while len(vs)<8:
  for x in (correct+d,correct-d):
   if x not in vs:vs.append(x)
   if len(vs)==8:break
  d+=1
 return list(map(str,vs))
def main():
 a=argparse.ArgumentParser();a.add_argument('--model',required=True);a.add_argument('--revision',required=True);a.add_argument('--manifest',required=True);a.add_argument('--output',required=True);a.add_argument('--max-tasks',type=int,default=0);a=a.parse_args()
 torch.set_num_threads(min(4,os.cpu_count() or 1));mb=Path(a.manifest).read_bytes();man=json.loads(mb);recs=man['records'][:a.max_tasks or None]
 info=model_info(a.model,revision=a.revision);tok=AutoTokenizer.from_pretrained(a.model,revision=a.revision);model=AutoModelForCausalLM.from_pretrained(a.model,revision=a.revision,torch_dtype=torch.float32,low_cpu_mem_usage=True);model.eval();start=time.time();rows=[]
 for no,r in enumerate(recs,1):
  target=tuple(tuple(map(int,z)) for z in r['target_polynomial']);opts=r['candidate_options'];cont=[o['expression'] for o in opts];ci=next(i for i,o in enumerate(opts) if o['pool_index']==r['target_pool_index']);row={'task_id':r['task_id'],'definition_cost':r['definition_cost'],'target_pool_index':r['target_pool_index']}
  for cond in ('active','random','passive'):
   sc=scores(model,tok,rank_prompt(r['evidence'][cond]),cont);rk=rank(sc,ci);row[f'recognition_{cond}_rank']=rk;row[f'recognition_{cond}_top1']=int(rk==1);row[f'recognition_{cond}_scores']=sc
  sc=scores(model,tok,teach_prompt(r['target_expression']),cont);rk=rank(sc,ci);row['teach_rank']=rk;row['teach_top1']=int(rk==1);row['teach_scores']=sc
  for cond in ('active','passive'):
   g=generate(model,tok,free_prompt(r['evidence'][cond]),64);p=parse_expr(g);row[f'free_{cond}_generation']=g;row[f'free_{cond}_parseable']=int(p is not None);row[f'free_{cond}_exact']=int(p==target);row[f'free_{cond}_parsed']=None if p is None else [list(z) for z in p]
  g=generate(model,tok,teach_prompt(r['target_expression']),64);p=parse_expr(g);row['teach_echo_generation']=g;row['teach_echo_parseable']=int(p is not None);row['teach_echo_exact']=int(p==target)
  labels=[o['label'] for o in r['query_choice']['query_options']];sc=scores(model,tok,query_prompt(r),labels);sel=max(range(len(sc)),key=lambda i:sc[i]['mean_logprob']);row['query_selected_label']=labels[sel];row['query_correct']=int(labels[sel] in r['query_choice']['correct_labels']);row['query_scores']=sc
  x,y=1,2;inner=val(target,x,y);correct=val(target,inner,y);ds=[]
  for o in opts:
   p=parse_expr(o['expression'])
   if p is not None:q=val(p,x,y);ds.append(val(p,q,y))
  nos=numeric_options(correct,ds);sc=scores(model,tok,transfer_prompt(r['target_expression'],x,y),nos);rk=rank(sc,nos.index(str(correct)));row['transfer_rank']=rk;row['transfer_top1']=int(rk==1);row['transfer_correct_value']=correct;row['transfer_options']=nos;row['transfer_scores']=sc;rows.append(row);print(a.model,no,'/',len(recs),r['task_id'],flush=True)
 metrics=['recognition_active_top1','recognition_random_top1','recognition_passive_top1','teach_top1','free_active_parseable','free_active_exact','free_passive_parseable','free_passive_exact','teach_echo_parseable','teach_echo_exact','query_correct','transfer_top1'];summary={k:float(np.mean([r[k] for r in rows])) for k in metrics}
 out={'benchmark':'JumpBench neural acquisition v0.1','model':a.model,'requested_revision':a.revision,'resolved_revision':info.sha,'parameter_count':sum(p.numel() for p in model.parameters()),'manifest_file_sha256':hashlib.sha256(mb).hexdigest(),'manifest_semantic_sha256':man.get('sha256_without_sha_field'),'n_tasks':len(rows),'summary':summary,'rows':rows,'runtime_seconds':time.time()-start,'environment':{'python':platform.python_version(),'torch':torch.__version__,'transformers':__import__('transformers').__version__}}
 Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'model':a.model,'summary':summary,'runtime_seconds':out['runtime_seconds']},indent=2))
if __name__=='__main__':main()
