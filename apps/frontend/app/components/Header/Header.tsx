import { useState, type ComponentProps, type ReactNode } from 'react';
import {
  CircleUserRound,
  EllipsisVertical,
  Languages,
  LogOut,
  Bell,
  FileText,
} from 'lucide-react';
import { Link, NavLink } from 'react-router';
import { Popover, PopoverContent, PopoverTrigger } from '../Popover/Popover';
import { useTranslation } from 'react-i18next';

import i18n from '../../i18n';
import { Tooltip, TooltipContent, TooltipTrigger } from '../Tooltip/Tooltip';

// Define user type for the header
type HeaderUser = {
  name: string;
  email?: string;
  role_name?: string;
};

function LanguageSelector() {
  const { t: tHeader } = useTranslation('header');

  const languages = Object.getOwnPropertyNames(
    tHeader('languages', { returnObjects: true })
  );

  return (
    <Popover>
      <PopoverTrigger asChild>
        <button type="button" className="cursor-pointer">
          <Languages size={24} className="text-primary" />
        </button>
      </PopoverTrigger>

      <PopoverContent>
        <ul className="flex flex-col gap-4">
          {languages.map(language => (
            <li key={language}>
              <button
                type="button"
                className="cursor-pointer"
                onClick={() => {
                  i18n.changeLanguage(language);
                }}
              >
                {tHeader(`languages.${language}`)}
              </button>
            </li>
          ))}
        </ul>
      </PopoverContent>
    </Popover>
  );
}

function UserMenu({ user }: { user?: HeaderUser | null }) {
  const { t: tHeader } = useTranslation('header');

  // If user is authenticated, show user dropdown menu
  if (user) {
    return (
      <Popover>
        <PopoverTrigger asChild>
          <button className="cursor-pointer flex items-center gap-2 p-2 hover:bg-gray-100 rounded-lg transition-colors">
            <CircleUserRound size={24} className="text-primary" />
            <span className="hidden sm:block text-sm text-gray-700">
              {user.name}
            </span>
          </button>
        </PopoverTrigger>

        <PopoverContent align="end" className="w-56">
          <div className="space-y-1">
            <div className="px-3 py-2 border-b border-gray-200">
              <p className="text-sm font-medium text-gray-900">{user.name}</p>
              {user.email && (
                <p className="text-xs text-gray-500">{user.email}</p>
              )}
              {user.role_name && (
                <p className="text-xs text-gray-500 capitalize">
                  {user.role_name}
                </p>
              )}
            </div>

            <Link
              to="/notifications"
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <Bell size={16} />
              {tHeader('notifications')}
            </Link>

            <Link
              to="/procedures"
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
            >
              <FileText size={16} />
              {tHeader('procedures')}
            </Link>

            <div className="border-t border-gray-200 pt-1">
              <Link
                to="/logout"
                className="flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
              >
                <LogOut size={16} />
                {tHeader('logout')}
              </Link>
            </div>
          </div>
        </PopoverContent>
      </Popover>
    );
  }

  // If user is not authenticated, show login link
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Link to="/login">
          <CircleUserRound size={24} className="text-primary" />
        </Link>
      </TooltipTrigger>

      <TooltipContent>{tHeader('login')}</TooltipContent>
    </Tooltip>
  );
}

function NavItems({
  navItems,
}: {
  navItems: ComponentProps<typeof Header>['navItems'];
}) {
  const { t: tHeader } = useTranslation('header');

  return navItems.map(({ translation, ...props }) => (
    <li key={translation}>
      <NavLink
        {...props}
        className={({ isActive }) =>
          `text-sm p-2 rounded-lg transition-colors ${
            isActive
              ? 'text-primary bg-primary/10 font-semibold'
              : 'text-zinc-700 hover:text-primary hover:bg-gray-100'
          }`
        }
      >
        {tHeader(`menu.${translation}`)}
      </NavLink>
    </li>
  ));
}

export function Header({
  navItems,
  logo,
  user,
}: {
  logo: ReactNode;
  user?: HeaderUser | null;
  navItems: Array<
    {
      translation: string;
    } & ComponentProps<typeof NavLink>
  >;
}) {
  const { t: tHeader } = useTranslation('header');
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-neutral-100 w-screen flex justify-center fixed top-0 inset-x-0 z-50 shadow-sm">
      <div className="container grid grid-cols-3 md:flex justify-between items-center p-4 min-h-16">
        <div className="flex gap-4 justify-start md:hidden">
          <Popover>
            <PopoverTrigger asChild>
              <button
                className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                aria-label={tHeader('mobileMenu')}
              >
                <EllipsisVertical size={24} className="text-primary" />
              </button>
            </PopoverTrigger>

            <PopoverContent align="start" className="w-56">
              <ul className="space-y-1">
                <NavItems navItems={navItems} />
              </ul>
            </PopoverContent>
          </Popover>

          <LanguageSelector />
        </div>

        <div className="flex justify-center items-center gap-4">{logo}</div>

        <nav className="box-border hidden md:block">
          <ul className="flex gap-2 justify-end items-center">
            <li className="flex items-center">
              <LanguageSelector />
            </li>

            <NavItems navItems={navItems} />

            <li className="flex items-center">
              <UserMenu user={user} />
            </li>
          </ul>
        </nav>

        <div className="md:hidden flex justify-end">
          <UserMenu user={user} />
        </div>
      </div>
    </header>
  );
}
