/** Alternative vector workflow. Uses the SAME numerical data as ManimGX, not hand drawn physics. */
import {makeScene2D, Path, Txt, Rect} from '@motion-canvas/2d';
import {createRef, all, waitFor} from '@motion-canvas/core';
import data from '../structural_data.json';

const base=(x:number,y:number):[number,number]=>[-540+x*128,225-y*128];
const orig=data.left_column.map(s=>base(s.x,s.y));
const displ=data.left_column.map(s=>base(s.x+data.geometry.amplification*s.dx,s.y+data.geometry.amplification*s.dy));
const asPath=(pts:[number,number][])=>pts.map(([x,y],i)=>`${i?'L':'M'} ${x.toFixed(2)} ${y.toFixed(2)}`).join(' ');
const moment=data.left_column.map(s=>[235+87*s.M/24,215-100*s.y] as [number,number]);

export default makeScene2D(function* (view){
  view.fill('#0B1524');
  const moved=createRef<Path>();
  const momentDraw=createRef<Path>();
  const state=createRef<Txt>();
  view.add(<>
    <Txt y={-410} text="DOBLE CURVATURA: EL PORQUÉ" fontSize={48} fontFamily="Arial" fontWeight={700} fill="#F3F7FC"/>
    <Txt x={-350} y={-340} fontSize={29} text="DEFORMADA · ×145" fontFamily="Arial" fill="#B9C9D9"/>
    <Txt x={330} y={-340} fontSize={29} text="MOMENTO LOCAL" fontFamily="Arial" fill="#B9C9D9"/>
    <Rect x={0} y={0} width={4} height={580} fill="#395169"/>
    <Path data={asPath(orig)} stroke="#55758A" lineWidth={6} lineDash={[15,10]}/>
    <Path ref={moved} data={asPath(displ)} stroke="#3BDCC4" lineWidth={12} end={0}/>
    <Path data="M 235 215 L 235 -125" lineWidth={4} stroke="#55758A"/>
    <Path ref={momentDraw} data={asPath(moment)} stroke="#FFDB91" lineWidth={8} end={0}/>
    <Txt x={355} y={250} text="-23,73 → +17,05 kN·m" fontFamily="Arial" fontSize={27} fill="#FFDB91"/>
    <Txt ref={state} y={385} text="Primero: el apoyo impide giro y traslación." fontFamily="Arial" fontSize={31} fill="#F3F7FC"/>
  </>);
  yield* moved().end(1,3.1);
  yield* state().text('Después: el momento cambia de signo.',.5);
  yield* momentDraw().end(1,2.9);
  yield* state().text('El punto de inflexión NO es una rótula.',.5);
  yield* waitFor(2);
});
