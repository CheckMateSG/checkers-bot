// components/defaultNavItems.tsx
import React from "react";
import { ChartBarIcon, CheckBadgeIcon, TrophyIcon } from "@heroicons/react/24/outline";
// define a NavItem prop
export type NavItem = {
  label: string;
  href: string;
  icon: React.ReactNode;
};
export const defaultNavItems: NavItem[] = [
  {
    label: "Dashboard",
    href: "/",
    icon: <ChartBarIcon className="w-6 h-6" />,
  },
  {
    label: "Votes",
    href: "../votes",
    icon: <CheckBadgeIcon className="w-6 h-6" />,
  },
  {
    label: "Achievements",
    href: "../achievements",
    icon: <TrophyIcon className="w-6 h-6" />,
  },
];