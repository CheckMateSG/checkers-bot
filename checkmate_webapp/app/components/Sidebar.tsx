import React from 'react';
import cn from "classnames";
import {
    ChevronDoubleLeftIcon, 
    ChevronDoubleRightIcon
} from "@heroicons/react/24/outline";
import {defaultNavItems, NavItem} from './NavItems';
import Link from 'next/link';
import Image from 'next/image';

type Props = {
    collapsed: boolean;
    navItems?:NavItem[];
    setCollapsed(collapsed: boolean):void;
    
};

const Sidebar = ({collapsed, navItems = defaultNavItems, setCollapsed}: Props) => {
    const Icon = collapsed ? ChevronDoubleRightIcon : ChevronDoubleLeftIcon;
    return (
        <div
      className={cn({
        "bg-orange-500 text-zinc-50 z-20": true,
        "transition-all duration-300 ease-in-out":true,
        "fixed md: static md: translate-x-0": true,
        "w-[250px]": !collapsed,
        "w-16": collapsed, 
        "h-full":true
      })}
    >
      <div
        className={cn({
          "flex flex-col justify-between": true,
          "h-full":true,
        })}
      >
        {/* logo and collapse button */}
        <div
          className={cn({
            "flex items-center border-b border-b-orange-500": true,
            "p-4 justify-between": !collapsed,
            "py-4 justify-center": collapsed,
          })}
        >
          <div className="flex gap-4 items-center h-11 overflow-hidden">
            {!collapsed && (
              <div className="flex gap-4 items-center">
                <Image
                  src="/logo-1.jpg"
                  alt="logo"
                  height={36}
                  width={36}
                  className="rounded-full"
                />
                <span className="text-white my-0">Sally</span>
              </div>
            )}
          </div>
          <button
            className={cn({
              "grid place-content-center": true, // position
              "hover:bg-orange-300 ": true, // color
              "w-10 h-10 rounded-full": true, // shape
            })}
            // 👇 set the collapsed state on click
            onClick={() => setCollapsed(!collapsed)}
          >
            <Icon className="w-5 h-5" />
          </button>
        </div>
        <nav className="flex-grow">
          <ul className={cn({"flex flex-col gap-4 items-stretch": true,})}>
            {navItems.map((item, index) => {
              return(
                <li key={index}
                className={cn({
                  "text-white text-center hover:bg-orange-300 flex": true,
                  "transition-colors duration-300":true, 
                  "rounded-md p2 mx-3 gap-4": !collapsed,
                  "rounded-full p-2 mx-3 w-10 h-10": collapsed,
                  "focus: ring-orange-300": true,
                })}
                >
                  <Link href={item.href} className="flex gap-2 items-center">
                    {item.icon} <span>{!collapsed && item.label}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>
      </div>
    </div>
);};

export default Sidebar;