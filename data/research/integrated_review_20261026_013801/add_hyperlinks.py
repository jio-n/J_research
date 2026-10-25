"""Add native hyperlinks after Artifact Tool export; do not rewrite content or styles."""
import pathlib,json,zipfile,xml.etree.ElementTree as E,collections
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];OUT=R/'outputs'/D.name
M='http://schemas.openxmlformats.org/spreadsheetml/2006/main';RNS='http://schemas.openxmlformats.org/officeDocument/2006/relationships';P='http://schemas.openxmlformats.org/package/2006/relationships'
E.register_namespace('',M);E.register_namespace('r',RNS)
for name in ['visit_plan.json','additional_workbook_plan.json']:
 p=json.loads((D/'_private'/(name+'.final.json')).read_text(encoding='utf-8'));file=OUT/p['fileName'];replacements={}
 with zipfile.ZipFile(file) as z:
  for i,s in enumerate(p['sheets'],1):
   links=[l for l in p['links'] if l['sheet']==s['name']]
   if not links:continue
   part=f'xl/worksheets/sheet{i}.xml';relpart=f'xl/worksheets/_rels/sheet{i}.xml.rels';root=E.fromstring(z.read(part))
   rel=E.fromstring(z.read(relpart)) if relpart in z.namelist() else E.Element('{'+P+'}Relationships')
   old=root.find('{'+M+'}hyperlinks')
   if old is not None:root.remove(old)
   hs=E.Element('{'+M+'}hyperlinks');seen=set()
   for j,l in enumerate(links,1):
    assert l['cell'] not in seen;seen.add(l['cell']);rid='IRHyperlink'+str(j)
    E.SubElement(rel,'{'+P+'}Relationship',Id=rid,Type=RNS+'/hyperlink',Target=l['url'],TargetMode='External')
    attrs={'ref':l['cell'],'{'+RNS+'}id':rid}
    if l.get('tip'):attrs['tooltip']=l['tip'][:250]
    E.SubElement(hs,'{'+M+'}hyperlink',attrs)
   after={'printOptions','pageMargins','pageSetup','headerFooter','rowBreaks','colBreaks','customProperties','cellWatches','ignoredErrors','smartTags','drawing','legacyDrawing','legacyDrawingHF','picture','oleObjects','controls','webPublishItems','tableParts','extLst'}
   idx=next((j for j,c in enumerate(root) if c.tag.split('}')[-1] in after),len(root));root.insert(idx,hs)
   replacements[part]=E.tostring(root,encoding='utf-8',xml_declaration=True);replacements[relpart]=E.tostring(rel,encoding='utf-8',xml_declaration=True)
  temp=D/'_private'/(name+'.linked.xlsx')
  with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as dest:
   for f in z.infolist():dest.writestr(f,replacements.pop(f.filename,z.read(f.filename)))
   for path,data in replacements.items():dest.writestr(path,data)
 temp.replace(file)
 print(json.dumps({'file':p['fileName'],'hyperlinks':len(p['links'])},ensure_ascii=False))
