import pathlib,json,zipfile,xml.etree.ElementTree as E,html,hashlib
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name;p=json.loads((D/'final_plan.json').read_text(encoding='utf8'));route=json.loads((D/'route_plan.json').read_text(encoding='utf8'));src=json.loads((D/'map_sources.json').read_text(encoding='utf8'));file=O/p['fileName']
M='http://schemas.openxmlformats.org/spreadsheetml/2006/main';RN='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PN='http://schemas.openxmlformats.org/package/2006/relationships';E.register_namespace('',M);E.register_namespace('r',RN)
with zipfile.ZipFile(file) as z:
 changes={}
 for i,s in enumerate(p['sheets'],1):
  ls=[l for l in p['links'] if l['sheet']==s['name']]
  if not ls:continue
  part=f'xl/worksheets/sheet{i}.xml';rpart=f'xl/worksheets/_rels/sheet{i}.xml.rels';root=E.fromstring(z.read(part));rel=E.fromstring(z.read(rpart)) if rpart in z.namelist() else E.Element('{'+PN+'}Relationships');old=root.find('{'+M+'}hyperlinks')
  if old is not None:root.remove(old)
  links=E.Element('{'+M+'}hyperlinks')
  for k,l in enumerate(ls):
   rid='VisitLink'+str(k);E.SubElement(rel,'{'+PN+'}Relationship',Id=rid,Type=RN+'/hyperlink',Target=l['url'],TargetMode='External');E.SubElement(links,'{'+M+'}hyperlink',{'ref':l['cell'],'{'+RN+'}id':rid,'tooltip':l.get('tip','')[:250]})
  after={'printOptions','pageMargins','pageSetup','headerFooter','drawing','legacyDrawing','tableParts','extLst'};idx=next((j for j,c in enumerate(root) if c.tag.split('}')[-1] in after),len(root));root.insert(idx,links);changes[part]=E.tostring(root,encoding='utf-8',xml_declaration=True);changes[rpart]=E.tostring(rel,encoding='utf-8',xml_declaration=True)
 tmp=D/'_private/linked.xlsx'
 with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as dest:
  for f in z.infolist():dest.writestr(f,changes.pop(f.filename,z.read(f.filename)))
  for k,v in changes.items():dest.writestr(k,v)
tmp.replace(file)
H=html.escape;rs=next(s for s in p['sheets'] if s['kind']=='route');colors={'黄色':'yellow','緑':'green','青系':'blue'}
def table(headers,rows):return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+H(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
areahtml=''
for a in route['areas']:
 code=a['area'][0];rows=[]
 for i,r in enumerate(rs['values']):
  if r[0]!=code:continue
  rows.append([f'<span class="{colors[rs["row_colors"][i]]}">{H(r[1])}</span>',H(r[2])+'<br>'+H(r[3]),H(r[6]).replace('\n','<br>'),H(r[7])])
 areahtml+=f'<section><h2>{H(a["area"])}</h2><p><strong>黄色の軸：</strong>{H(a["core"])}</p><p>{H(a["move"])}</p><p><strong>追加の選び方：</strong>{H(a["optional"])}</p><p class="cut"><strong>時間がなければ：</strong>{H(a["cut"])}</p><p><a href="{H(src["pdfs"][a["map"]])}">公式小間図を開く</a></p>'+table(['優先・巡回','企業・ブース','見る展示','寄り方・確認事項'],rows)+'</section>'
body=f'''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>JIMTOF2026 訪問先更新版と巡回案</title><style>body{{font:16px/1.8 "Yu Gothic UI",Meiryo,sans-serif;margin:0;color:#263743;background:#f2f5f7}}header,main{{max-width:1200px;margin:auto;padding:24px}}header{{background:#183f52;color:white}}section{{background:white;padding:24px;margin:20px 0}}h1{{font-size:27px}}h2{{font-size:23px}}a{{color:#075a96}}header a{{color:#ccefff}}.scroll{{overflow:auto}}table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{border:1px solid #cad5dc;padding:12px;vertical-align:top;min-width:130px}}th{{background:#e6eef3;text-align:left}}td:last-child{{min-width:270px}}.yellow,.green,.blue{{display:inline-block;padding:4px 8px;color:#17313b}}.yellow{{background:#ffff00}}.green{{background:#d9ead3}}.blue{{background:#cfe2f3}}.cut{{border-left:4px solid #c29126;padding-left:14px}}li{{margin-bottom:9px}}@media(max-width:600px){{header,main{{padding:14px}}section{{padding:16px}}h1{{font-size:23px}}}}@media print{{body{{background:white}}section{{break-inside:avoid}}}}</style><header><p>2026-10-26／手持ち写真4枚を反映・視察前</p><h1>黄色11社を軸に、近隣候補を選ぶ巡回案</h1><p>訪問予定34社、新規9社10アイテム。色なし15社は履歴へ、元一覧の未精査20社は別保持。</p><p><a href="{H(p['fileName'])}">訪問先一覧の更新版Excelを開く</a></p></header><main><section><h2>まず回る順番</h2><p><strong>東1 → 東2を通過 → 東3 → 東8 → 東7 → 南2 → 南3</strong>。入口未指定のため東側開始の案。南4・南1・西は残時間で追加する。</p><ol><li>東1：マザック E1001 → CAMSUPS E1053</li><li>東3：シーメンス E3006 → オークマ E3028</li><li>東8・7：DMG森精機 E8005 → ハイデンハイン E7043 → ナガセ E7097</li><li>南2：ファナック S2001 → 三菱電機 S2003</li><li>南3：たけびし S3015 → モリマシナリー S3048</li></ol><p>東2には黄色がないため、通過時にベッコフ・シマダ・Hexagonなどから選ぶ。黄色の実演予定があれば、同じエリア内で順番を入れ替える。</p><p class="cut">黄色だけでも、1社20～30分なら220～330分。移動・待ち60～90分、休憩45分を仮置きすると<strong>約5時間25分～7時間45分</strong>。これは実測値ではない。34社すべてを回る前提にせず、緑はまず3～5社、青は残時間で選ぶ。</p><p><strong>緑を絞るなら：</strong>加工結果のフィードバックを比較するTPR、入力形状から経路を作る東京エレクトロンデバイス、CNCへの機能組込を見るベッコフ、工程・見積判断を見る匠技研などから関心に合わせて選ぶ。各社が互いに隣接するという意味ではない。</p><p><strong>二日なら：</strong>1日目を東1～3・東7～8、2日目を南2・南3と追加エリアに分ける。</p></section><section><h2>棟間移動と省略のルール</h2><ul><li>公式全体図には無料巡回バス「中央ターミナル→東7→南2→中央ターミナル」が案内されている。東7→南2区間を利用候補にする。運行・混雑・待ち時間は当日確認。</li><li>南1・2は1F、南3・4は4F。西1・2は1F、西3・4は4F。ホール番号順だけでは移動を最適化できない。</li><li>西には今回の黄色なし。THK・ナベル・Wintechのためだけに別棟へ移るのは余裕がある場合。</li><li>東4～6は改修休館の表示。通常展示ホールとして横切る案は作っていない。</li><li>Wintechは写真1の緑と写真3の青をシート別に保持。巡回表では青の保留枠とした。</li></ul><p><a href="https://www.jimtof.org/jp/exhi_search_booth.html">公式小間割図検索</a> ／ <a href="https://jimtof.org/files/site_map_jp.pdf">公式会場全体図</a></p></section>{areahtml}<section><h2>新版Excelの扱い</h2><p>先頭2シートは編集・検索用、閲覧_は企業・ブースを縦結合した同時点の複製。新規行の着眼点と当日質問は本人の追記待ちで空欄。旧優先欄の文章・★等は消さず、行の色で今回の優先度を反映。写真にない未精査候補を対象外とはしていない。</p><p>本案は公開小間図の配置に基づく地域ごとの順序案。通路の実測距離、最短経路、実演待ち、移動所要時間は未検証。展示未確認のアイテムはその注記を保持。</p></section></main></html>'''
(O/'巡回順とエリア別訪問案.html').write_text(body,encoding='utf8')
manifest={'source_workbook':p['source_workbook'],'source_sha256':p['source_sha256'],'counts':p['counts'],'new_companies':p['new_companies'],'new_items':p['new_items'],'route_core':route['core_route'],'preserved_fields':'既存A:Iの全値と全リンクを保持。変更は行の色、訪問予定と履歴・未精査の区分、新規行、巡回表。','remaining':'Wintechのシート間優先色差／サイバーRCの小間表記差／個別展示と実演時刻／未掲載候補全体の精査'}
(D/'update_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'xlsx':p['fileName'],'hyperlinks':len(p['links']),'html':'巡回順とエリア別訪問案.html'},ensure_ascii=False))
