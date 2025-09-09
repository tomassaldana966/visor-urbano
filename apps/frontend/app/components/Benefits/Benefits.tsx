import { useTranslation } from 'react-i18next';

export function Benefits() {
  const { t: tBenefits } = useTranslation('benefits');

  const benefits = tBenefits('benefits', {
    returnObjects: true,
    defaultValue: [],
  }) as string[];

  return (
    <section className="grid grid-cols-1 md:grid-cols-10 container gap-8">
      <div
        className="bg-contain bg-no-repeat w-full h-40 md:h-full md:col-span-4 bg-center"
        style={{
          backgroundImage: 'url(/background/benefits.png)',
        }}
      />

      <div className="md:col-span-6 md:col-start-5 flex flex-col gap-8">
        <h1 className="text-4xl md:text-5xl">{tBenefits('title')}</h1>

        <ul className="flex flex-col gap-4 px-4">
          {benefits.map(benefit => (
            <li key={benefit} className="flex gap-4 items-center text-xl">
              <div className="bg-primary rounded-full h-1 w-1" />

              {benefit}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
