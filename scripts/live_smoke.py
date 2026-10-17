import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as contract_actions

def calldata_compat(method=None,args=None,kwargs=None):
 out={}
 if method is not None:out['method']=method
 if args:out['args']=args
 if kwargs:out['kwargs']=kwargs
 return out
contract_actions.make_calldata_object=calldata_compat
ROOT=Path(__file__).parents[1];ENV=(ROOT.parents[3]/'accounts.env').read_text(encoding='utf-8')
def account(number):
 key=re.search(rf'^ACCOUNT_{number}_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip();return create_account(account_private_key=key)
def client(number):return create_client(chain=studionet,account=account(number))
ADDRESS=json.loads((ROOT/'deployment.json').read_text(encoding='utf-8'))['contractAddress']
def finalized(number,name,args,expected='SUCCESS'):
 c=client(number);tx=c.write_contract(address=ADDRESS,function_name=name,args=args);print(name+'_tx='+str(tx),flush=True)
 receipt=c.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True);leader=(receipt.get('consensus_data',{}).get('leader_receipt') or [{}])[0]
 assert receipt.get('result_name')=='MAJORITY_AGREE' and leader.get('execution_result')==expected,receipt
 return str(tx),leader
stamp=str(int(time.time()));review_id='BUDGET-'+stamp;base='https://cdn.jsdelivr.net/gh/SAMiiNW/ambiguity-budget@main/fixtures/'
dimensions=['Exact production launch date and time','Closed set of allowed launch regions','Role with exclusive final production approval','Named rollback ownership role']
open_tx,_=finalized(1,'open_review',[review_id,account(2).address,'Dispatch specification ambiguity gauge',dimensions,0,base+'draft-spec.md'])
evaluate_tx,_=finalized(1,'evaluate',[review_id]);draft=client(1).read_contract(address=ADDRESS,function_name='get_review',args=[review_id])
assert draft['state']=='NEEDS_REVISION' and draft['score']==5 and draft['statuses']==['MULTIPLE','RESOLVED','MISSING','RESOLVED'],draft
revise_tx,_=finalized(2,'revise',[review_id,base+'revised-spec.md']);clear=client(1).read_contract(address=ADDRESS,function_name='get_review',args=[review_id])
assert clear['state']=='CLEAR' and clear['score']==0 and clear['round']==2 and clear['statuses']==['RESOLVED']*4,clear
before=clear;replay_tx,replay_leader=finalized(2,'revise',[review_id,base+'revised-spec.md'],expected='ERROR');after=client(1).read_contract(address=ADDRESS,function_name='get_review',args=[review_id]);assert before==after
transactions={'openReview':open_tx,'evaluateDraft':evaluate_tx,'reviseToClear':revise_tx,'postClearReplayRejected':replay_tx}
proof={'reviewId':review_id,'transactions':transactions,'explorer':{k:'https://explorer-studio.genlayer.com/transactions/'+v for k,v in transactions.items()},'negativeExecution':replay_leader.get('execution_result'),'stateUnchangedAfterReplay':before==after,'draft':draft,'final':clear,'fixtureDisclosure':'Both specification files and both demonstration wallets are operator-controlled fixtures used to prove monotonic ambiguity reduction; they are not independent third-party attestations.'}
(ROOT/'evidence').mkdir(exist_ok=True);(ROOT/'evidence'/'live-run.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8');print(json.dumps(proof,indent=2),flush=True)
