// src/components/MainContent.jsx
import React from 'react';
import ReactLogo from '/public/react.svg';

const MainContent = () => {
    return (
        <main className='flex-auto bg-gray-200 p-4 text-black'>
            <img src={ReactLogo} alt='React Logo' className='h-24 w-24 mx-auto' />
            <h1 className='text-2xl font-bold'>Fun Facts about React!</h1>
            <ul className='text-lg list-disc items-center px-10 inline-block list-inside'> These are the reasons for the popularity of React:
                <li > It is fun</li>
                <li> It is popular</li>
                <li> It is easy to learn</li>
                <li> It is easy to use</li>
                <li> It is fast</li>
            </ul>
        </main>
    );
};

export default MainContent;