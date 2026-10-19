// 最小のデータ整合性確認。iPhone / DOM の実機検証を代替しない。
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script); // JS 構文確認
const elements = {};
const storage = {};
const context = vm.createContext({
  TextEncoder, TextDecoder, Uint8Array, DataView, Blob, setTimeout,
  document: { getElementById: id => elements[id] ||= {value:'', innerHTML:'', textContent:''} },
  localStorage: {getItem:k=>storage[k]||null,setItem:(k,v)=>storage[k]=v},
  window: {addEventListener(){}}, navigator: {}, alert: () => {}, confirm: () => true
});
vm.runInContext(script, context);
vm.runInContext(`
selected = 'sample-a';
addItem(state.companies[0].candidates[0]);
record().memo = '保存テスト';
record().items[0].attachments.push({name:'test.wav',data:'data:audio/wav;base64,VEVTVA=='});
save();
if (!valid(JSON.parse(localStorage.getItem(KEY)))) throw Error('保存形式不整合');
if (state.companies[0].candidates.length !== 1 || record().items.length !== 1) throw Error('候補追加不整合');
var backup = JSON.stringify(state);
var zip = zipStore(backup);
if (unzipStore(zip.buffer) !== backup) throw Error('ZIP 往復不一致');
var bad = zip.slice(); bad[45] ^= 1;
var rejected = false; try { unzipStore(bad.buffer); } catch { rejected = true; }
if (!rejected) throw Error('破損 ZIP を受理');
var rows = parseCSV('year,company_name,booth\\r\\n2026,"A,B",E01\\r\\n');
if (normalizeCompany(rows[0],0,'').name !== 'A,B') throw Error('CSV 不整合');
`, context);
assert.ok(storage['jimtof-field-poc-v1']);
console.log('PASS: JS 構文、候補の明示追加、添付込み保存形式、ZIP 往復・破損検出、CSV 引用符');
