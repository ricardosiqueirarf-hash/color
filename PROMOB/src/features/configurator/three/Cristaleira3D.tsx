import type { CristaleiraCalculation, CristaleiraConfig } from '../types/configuratorTypes';
import { aluminumColors, glasses } from '../data/catalog';

const mm = (value: number) => value / 1000;

export function Cristaleira3D({ config, calculation }: { config: CristaleiraConfig; calculation: CristaleiraCalculation }) {
  const w = mm(config.widthMm);
  const h = mm(config.heightMm);
  const d = mm(config.depthMm);
  const side = mm(config.sideMdfMm);
  const top = mm(config.topMdfMm);
  const shelf = mm(config.shelfThicknessMm);
  const uw = mm(calculation.useful.usefulWidthMm);
  const uh = mm(calculation.useful.usefulHeightMm);
  const ud = mm(calculation.useful.usefulDepthMm);
  const mdf = '#7a5232';
  const metal = aluminumColors[config.aluminumColor];
  const glass = glasses[config.glassId as keyof typeof glasses];

  return (
    <group position={[0, h / 2, 0]}>
      <Box pos={[-w / 2 + side / 2, 0, 0]} size={[side, h, d]} color={mdf} />
      <Box pos={[w / 2 - side / 2, 0, 0]} size={[side, h, d]} color={mdf} />
      <Box pos={[0, h / 2 - top / 2, 0]} size={[w, top, d]} color={mdf} />
      <Box pos={[0, -h / 2 + top / 2, 0]} size={[w, top, d]} color={mdf} />
      {config.hasBackPanel && <Box pos={[0, 0, -d / 2 + mm(config.backMdfMm) / 2]} size={[w, h, mm(config.backMdfMm)]} color="#4b2f1c" />}
      {Array.from({ length: config.shelfCount }).map((_, index) => {
        const y = -uh / 2 + ((index + 1) * uh) / (config.shelfCount + 1);
        return <Box key={index} pos={[0, y, 0]} size={[uw, shelf, ud]} color="#8b623e" />;
      })}
      {Array.from({ length: config.doorCount }).map((_, index) => {
        const doorW = mm(calculation.door.widthMm);
        const x = -uw / 2 + doorW / 2 + index * (uw / config.doorCount);
        return <Door key={index} x={x} y={0} z={d / 2 + 0.012 + index * 0.006} w={doorW} h={uh} metal={metal} glassColor={glass.color} opacity={glass.opacity} />;
      })}
    </group>
  );
}

function Door(props: { x: number; y: number; z: number; w: number; h: number; metal: string; glassColor: string; opacity: number }) {
  const bar = 0.035;
  return (
    <group position={[props.x, props.y, props.z]}>
      <Box pos={[0, 0, 0]} size={[props.w - bar * 2, props.h - bar * 2, 0.01]} color={props.glassColor} opacity={props.opacity} />
      <Box pos={[0, props.h / 2 - bar / 2, 0.015]} size={[props.w, bar, 0.03]} color={props.metal} />
      <Box pos={[0, -props.h / 2 + bar / 2, 0.015]} size={[props.w, bar, 0.03]} color={props.metal} />
      <Box pos={[-props.w / 2 + bar / 2, 0, 0.015]} size={[bar, props.h, 0.03]} color={props.metal} />
      <Box pos={[props.w / 2 - bar / 2, 0, 0.015]} size={[bar, props.h, 0.03]} color={props.metal} />
    </group>
  );
}

function Box({ pos, size, color, opacity = 1 }: { pos: [number, number, number]; size: [number, number, number]; color: string; opacity?: number }) {
  return (
    <mesh position={pos}>
      <boxGeometry args={size} />
      <meshStandardMaterial color={color} transparent={opacity < 1} opacity={opacity} roughness={0.45} metalness={0.08} />
    </mesh>
  );
}
