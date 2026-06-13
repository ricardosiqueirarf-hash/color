import { calculateCristaleira } from '../logic/calculateCristaleira';
import { useConfiguratorStore } from '../store/configuratorStore';
import { ConfiguratorForm } from './ConfiguratorForm';
import { ResultPanel } from './ResultPanel';
import { Scene3D } from '../three/Scene3D';

export function ConfiguratorPage() {
  const config = useConfiguratorStore((state) => state.config);
  const updateConfig = useConfiguratorStore((state) => state.updateConfig);
  const calculation = calculateCristaleira(config);

  return (
    <main className="app-shell">
      <ConfiguratorForm config={config} onChange={updateConfig} />
      <section className="center-panel">
        <header className="topbar">
          <div>
            <h1>Configurador ColorGlass</h1>
            <p>MVP técnico para orçamento 3D de cristaleira.</p>
          </div>
        </header>
        <Scene3D config={config} calculation={calculation} />
      </section>
      <ResultPanel calculation={calculation} />
    </main>
  );
}
