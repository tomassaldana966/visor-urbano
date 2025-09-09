import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: '🌍 Implementación Global',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Visor Urbano está diseñado para gobiernos municipales de todo el mundo.
        Nuestra documentación proporciona guías específicas por ciudad para
        implementación, adaptación y mejores prácticas.
      </>
    ),
  },
  {
    title: '🏛️ Enfoque Municipal',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Construido específicamente para departamentos de planificación urbana,
        oficinas de permisos y servicios municipales. Optimiza tus procesos y
        mejora el servicio ciudadano.
      </>
    ),
  },
  {
    title: '🚀 Listo para Producción',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Con implementaciones exitosas en múltiples municipalidades, nuestro
        sistema está probado en batalla y listo para despliegue en tu ciudad.
      </>
    ),
  },
];

function Feature({ title, Svg, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
