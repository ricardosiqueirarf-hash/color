import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Cristaleira3D } from './Cristaleira3D';
import type { CristaleiraCalculation, CristaleiraConfig } from '../types/configuratorTypes';

export function Scene3D(props: { config: CristaleiraConfig; calculation: CristaleiraCalculation }) {
  return (
    <div className="scene-wrap">
      <Canvas>
        <ambientLight intensity={0.8} />
        <directionalLight position={[3, 4, 5]} intensity={1} />
        <Cristaleira3D config={props.config} calculation={props.calculation} />
        <OrbitControls />
      </Canvas>
    </div>
  );
}
