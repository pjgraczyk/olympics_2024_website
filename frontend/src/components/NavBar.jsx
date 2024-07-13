// src/components/NavBar.jsx
import React from 'react';

const NavBar = () => {
    return (
        <nav className='flex-auto bg-gray-800 text-white text-center p-4'>
            <ul className='flex text-white text-large justify-around px-10 [&>*]:p-4'>
                <li> Home </li>
                <li> About </li>
                <li> Recent </li>
            </ul>
        </nav>
    );
};

export default NavBar;