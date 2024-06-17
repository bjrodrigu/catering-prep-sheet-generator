import React from 'react';
import './App.css';

const Header = () => {
    return (
        <header className="site-header">
            <div className="header-content">
                <h1 className="site-title">Catering Execution Generator</h1>
                <nav className="site-nav">
                    <ul className="nav-list">
                        <li className="nav-item"><a href="/" className="nav-link">Home</a></li>
                        <li className="nav-item"><a href="/tutorial" className="nav-link">Tutorial</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    );
};

export default Header;