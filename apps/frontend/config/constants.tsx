import { Link } from 'react-router';

export const footerNav = {
  es: [
    <Link
      key="1"
      to="https://congresoweb.congresojal.gob.mx/BibliotecaVirtual/LeyesEstatales.cfm"
      rel="noopener noreferrer"
    >
      Normatividad
    </Link>,
    <Link key="2" to="https://datos.jalisco.gob.mx/" rel="noopener noreferrer">
      Datos abiertos
    </Link>,
    <img
      src="/logos/Logo-Municipal.svg"
      alt="Jalisco"
      key="3"
      className="h-22 w-auto hidden md:block"
    />,
  ],
  en: [
    <Link
      key="1"
      to="https://congresoweb.congresojal.gob.mx/BibliotecaVirtual/LeyesEstatales.cfm"
      rel="noopener noreferrer"
    >
      Regulations
    </Link>,
    <Link key="2" to="https://datos.jalisco.gob.mx/" rel="noopener noreferrer">
      Open data
    </Link>,
    <img
      src="/logos/Logo-Municipal.svg"
      alt="Jalisco"
      key="3"
      className="h-16 w-auto hidden md:block"
    />,
  ],
  fr: [
    <Link
      key="1"
      to="https://congresoweb.congresojal.gob.mx/BibliotecaVirtual/LeyesEstatales.cfm"
      rel="noopener noreferrer"
    >
      Réglementations
    </Link>,
    <Link key="2" to="https://datos.jalisco.gob.mx/" rel="noopener noreferrer">
      Données ouvertes
    </Link>,
    <img
      src="/logos/jalisco.svg"
      alt="Jalisco"
      key="3"
      className="h-10 hidden md:block"
    />,
  ],
  pt: [
    <Link
      key="1"
      to="https://congresoweb.congresojal.gob.mx/BibliotecaVirtual/LeyesEstatales.cfm"
      rel="noopener noreferrer"
    >
      Regulamentos
    </Link>,
    <Link key="2" to="https://datos.jalisco.gob.mx/" rel="noopener noreferrer">
      Dados abertos
    </Link>,
    <img
      src="/logos/jalisco.svg"
      alt="Jalisco"
      key="3"
      className="h-10 hidden md:block"
    />,
  ],
} as const;

export const Logo = (
  <img src="/logos/jalisco.svg" alt="Jalisco" className="h-10" />
);
