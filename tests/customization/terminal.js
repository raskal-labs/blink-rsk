const fs = require('fs'), vm = require('vm'), assert = require('assert');
const completeSource = fs.readFileSync(process.argv[2], 'utf8');
const source = completeSource.split('var _workbenchSelecting = false;')[1];
assert(source);
const rows = [{text:'wrapped',o:true}, {text:' continuation 👩🏽‍💻',o:false}, {text:'quote\'s $() literal',o:false}, {text:'last',o:false}];
let scrolls=0;
const context = {t:{getRowCount:()=>rows.length, screenSize:{height:2},getRowNode:i=>rows[i],
 getRowsText:(start,end)=>rows.slice(start,end).map((r,i)=>r.text+(i<end-start-1&&!r.o?'\n':'')).join(''),scrollEnd:()=>scrolls++}};
vm.createContext(context);vm.runInContext('var _workbenchSelecting = false;'+source,context);
let a=context.term_workbenchRows(false,0,1), b=context.term_workbenchRows(false,1,128);
assert(a.continued);assert.equal(a.text+b.text,'wrapped continuation 👩🏽‍💻\nquote\'s $() literal\nlast');
const screen=context.term_workbenchRows(true,0,128);assert.equal(screen.text,"quote's $() literal\nlast");assert.equal(screen.total,2);
assert.equal(context.term_workbenchRows(false,0,0).text,'');
context.term_workbenchBottom();assert.equal(scrolls,1);
for(const visibleFirst of [true,false]) for(const visibleLast of [true,false]) {
 let first={rowIndex:0,childNodes:[1]},last={rowIndex:3,childNodes:[1,2]},firstArg,lastArg;
 let top={nextSibling:visibleFirst?first:{rowIndex:1},previousSibling:visibleFirst?null:{}},bottom={previousSibling:visibleLast?last:{rowIndex:2},nextSibling:visibleLast?null:{}};
 let port={topFold_:top,bottomFold_:bottom,rowNodes_:{removeChild:()=>{top.previousSibling=null;bottom.nextSibling=null},insertBefore:()=>{},appendChild:()=>{}},fetchRowNode_:i=>i===0?first:last,syncRowNodesDimensions_:()=>{},
 document_:{getSelection:()=>({collapse:(node,offset)=>{firstArg=node;assert.equal(offset,0)},extend:(node,offset)=>{lastArg=node;assert.equal(offset,2)}})},selection:{sync:()=>{}}};
 context.t.scrollPort_=port;context.term_workbenchSelectAll();assert.strictEqual(firstArg,first);assert.strictEqual(lastArg,last);
}
rows.length=0;assert.equal(context.term_workbenchRows(false,0,128).total,0);context.term_workbenchSelectAll();
console.log('PASS: retained-row Unicode/wrap preservation, screen scope, empty/zero-count capture, bottom jump and all four Select All first/last visibility branches');

// Execute the actual native gesture reporters, rather than duplicating their guards.
let reports=[];
context.MouseEvent=function(name,options){this.name=name;Object.assign(this,options)};
context.WheelEvent=context.MouseEvent;
context._setTermCoordinates=()=>{};
context.term_displayInput=()=>{};
context.name='click';
context.t.prompt={processMouseClick:()=>{reports.push('click');return true}};
context.t.onMouse=()=>reports.push('mouse');
context.t.onMouse_Blink=()=>reports.push('wheel');
for(const fn of ['term_reportMouseClick','term_reportMouseEvent','term_reportWheelEvent']) {
 const start=completeSource.indexOf('function '+fn+'(');
 const end=completeSource.indexOf('\nfunction ',start+1);
 assert(start>=0&&end>start);vm.runInContext(completeSource.slice(start,end),context);
}
function report(){context.term_reportMouseClick(1,2,1,false);context.term_reportMouseEvent('mousedown',1,2,1);context.term_reportWheelEvent('wheel',1,2,0,1)}
report();assert.deepStrictEqual(reports,['click','mouse','wheel']);
context.term_workbenchSetInteraction(true);report();assert.equal(reports.length,3);
context.term_workbenchSetInteraction(false);report();assert.equal(reports.length,6);
console.log('PASS: Select/Scroll suppresses click, mouse and wheel terminal input; Input mode restores all three reporters');
