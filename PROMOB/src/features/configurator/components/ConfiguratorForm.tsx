import type { CristaleiraConfig } from '../types/configuratorTypes';

type Patch = Partial<CristaleiraConfig>;

export function ConfiguratorForm({ config, onChange }: { config: CristaleiraConfig; onChange: (patch: Patch) => void }) {
  const n = (key: keyof CristaleiraConfig) => (event: React.ChangeEvent<HTMLInputElement>) => onChange({ [key]: Number(event.target.value) } as Patch);
  const s = (key: keyof CristaleiraConfig) => (event: React.ChangeEvent<HTMLSelectElement>) => onChange({ [key]: event.target.value } as Patch);

  return (
    <aside className="panel left-panel">
      <h2>Cristaleira</h2>
      <label>Altura mm<input type="number" value={config.heightMm} onChange={n('heightMm')} /></label>
      <label>Largura mm<input type="number" value={config.widthMm} onChange={n('widthMm')} /></label>
      <label>Profundidade mm<input type="number" value={config.depthMm} onChange={n('depthMm')} /></label>
      <label>MDF laterais<input type="number" value={config.sideMdfMm} onChange={n('sideMdfMm')} /></label>
      <label>MDF superior<input type="number" value={config.topMdfMm} onChange={n('topMdfMm')} /></label>
      <label>MDF inferior<input type="number" value={config.bottomMdfMm} onChange={n('bottomMdfMm')} /></label>
      <label>Prateleiras<input type="number" value={config.shelfCount} onChange={n('shelfCount')} /></label>
      <label>Portas<input type="number" value={config.doorCount} onChange={n('doorCount')} /></label>
      <label>Abertura<select value={config.openingType} onChange={s('openingType')}><option value="giro">Giro</option><option value="correr">Correr</option></select></label>
      <label>Perfil<select value={config.profileId} onChange={s('profileId')}><option value="1036">1036</option><option value="070">070</option><option value="3545">3545</option><option value="3446">3446</option></select></label>
      <label>Vidro<select value={config.glassId} onChange={s('glassId')}><option value="incolor">Incolor</option><option value="espelho_prata">Espelho prata</option><option value="reflecta_bronze">Reflecta bronze</option><option value="reflecta_prata">Reflecta prata</option><option value="fume">Fumê</option></select></label>
      <label>Margem<input type="number" value={config.marginPercent} onChange={n('marginPercent')} /></label>
    </aside>
  );
}
