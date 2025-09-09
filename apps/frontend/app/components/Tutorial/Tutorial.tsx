import { useTranslation } from 'react-i18next';

export function Tutorial() {
  const { t: tTutorial } = useTranslation('tutorial');

  return (
    <section className="flex flex-col gap-8 container">
      <h1 className="text-4xl md:text-5xl text-center">{tTutorial('title')}</h1>

      <iframe
        className="rounded-xl overflow-hidden aspect-video"
        width="100%"
        height="100%"
        src={`https://www.youtube.com/embed/${tTutorial('youTubeVideID')}`}
        title="YouTube video player"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerPolicy="strict-origin-when-cross-origin"
        allowFullScreen
      />
    </section>
  );
}
