import React from 'react';
import {Composition,AbsoluteFill,interpolate,useCurrentFrame,useVideoConfig} from 'remotion';
const EndCard=()=>{
 const frame=useCurrentFrame();const {fps}=useVideoConfig();
 const fade=interpolate(frame,[0,12,6*fps-20,6*fps-2],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <AbsoluteFill style={{backgroundColor:'#0B1524',fontFamily:'Arial',alignItems:'center',justifyContent:'center',color:'#F3F7FC',opacity:fade}}>
  <div style={{fontSize:28,letterSpacing:4,color:'#3BDCC4'}}>LABORATORIO DE ESTRUCTURAS</div>
  <div style={{fontSize:75,fontWeight:750,marginTop:16}}>Primero comprende. Después calcula.</div>
  <div style={{fontSize:30,marginTop:35,color:'#B9C9D9'}}>Deformada • Curvatura • Momento • Cortante</div>
  <div style={{fontSize:23,marginTop:30,color:'#80BBFF'}}>Ejemplo didáctico · No es una memoria de cálculo</div>
 </AbsoluteFill>;
};
export const Root=()=> <Composition id="endcard" component={EndCard} durationInFrames={180} fps={30} width={1920} height={1080}/>;
