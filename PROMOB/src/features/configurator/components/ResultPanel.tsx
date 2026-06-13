import type { CristaleiraCalculation } from '../types/configuratorTypes';

export function ResultPanel({ calculation }: { calculation: CristaleiraCalculation }) {
  return (
    <aside className="panel right-panel">
      <h2>Resultado tecnico</h2>
      <p>Vao util: {Math.round(calculation.useful.usefulWidthMm)} x {Math.round(calculation.useful.usefulHeightMm)} mm</p>
      <p>Cada porta: {Math.round(calculation.door.widthMm)} x {Math.round(calculation.door.heightMm)} mm</p>
      <p>Vidro total: {calculation.totalGlassAreaM2.toFixed(2)} m2</p>
      <p>Perfil total: {calculation.totalProfileMl.toFixed(2)} m</p>
      <p>Baguete total: {calculation.totalBaguetteMl.toFixed(2)} m</p>
      <p>Area MDF: {calculation.mdfAreaM2.toFixed(2)} m2</p>
      <p>Custo estimado: R$ {calculation.subtotalCost.toFixed(2)}</p>
      <p>Venda sugerida: R$ {calculation.salePrice.toFixed(2)}</p>
    </aside>
  );
}
