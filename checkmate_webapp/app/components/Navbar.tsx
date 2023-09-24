// components/Navbar.tsx
import React from "react";
import { Bars3Icon } from "@heroicons/react/24/outline";
import classNames from "classnames";

const Navbar = () => {
  return (
    <nav
      className={classNames({
        "bg-white text-zinc-500": true, // colors
        "flex items-center": true, // layout
        // "p-8": true,
        "w-screen sticky z-10 px-4 shadow-sm h-[72px] top-0 ": true, //positioning & styling
        // "col-start-2": true,
      })}
    >
      <div className="font-bold text-lg text-orange-500">Checkmate</div>
      {/* <div className="flex-grow"></div> */}
    </nav>
  );
};
export default Navbar;

