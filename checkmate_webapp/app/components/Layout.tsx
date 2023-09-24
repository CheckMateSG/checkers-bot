"use client"

import React, {PropsWithChildren, useState} from 'react';
import classNames from 'classnames';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

const Layout = (props: PropsWithChildren) => {
    const [collapsed, setSidebarCollapsed] = useState(false);
    
    return (
        <div className = {classNames({
            "grid min-h-screen": true,
            "grid-cols-sidebar": !collapsed,
            "grid-cols-sidebar-collapsed": collapsed, 
            "transition-[grid-template-columns] duration-300 ease-in-out": true,
        })}
        >
            <Navbar />
            <Sidebar 
                collapsed={!collapsed}
                setCollapsed = {() => setSidebarCollapsed((prev)=>!(prev))}
            />
            
            
            {props.children}
        </div>
    );
};

export default Layout;