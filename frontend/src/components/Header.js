import { Link, useLocation } from 'react-router-dom';
import { Shield, Menu, X, Phone } from 'lucide-react';
import { useState } from 'react';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Services', path: '/services' },
    { name: 'Blog', path: '/blog' },
    { name: 'About', path: '/about' },
    { name: 'Contact', path: '/contact' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group" data-testid="header-logo">
            <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center transform group-hover:scale-105 transition-transform">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-slate-900">Dr. Kishan Bhalani</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                data-testid={`nav-${link.name.toLowerCase()}`}
                className={`text-sm font-medium transition-colors relative group ${
                  isActive(link.path)
                    ? 'text-teal-600'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {link.name}
                <span
                  className={`absolute -bottom-1 left-0 w-full h-0.5 bg-teal-600 transform origin-left transition-transform ${
                    isActive(link.path) ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'
                  }`}
                />
              </Link>
            ))}
          </nav>

          {/* CTA Button */}
          <Link
            to="/contact"
            data-testid="header-cta-button"
            className="hidden md:flex items-center space-x-2 bg-teal-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-teal-700 transition-all hover:shadow-lg hover:shadow-teal-600/30 transform hover:-translate-y-0.5"
          >
            <Phone className="w-4 h-4" />
            <span>Free Case Review</span>
          </Link>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-slate-100 transition-colors"
            data-testid="mobile-menu-button"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white" data-testid="mobile-menu">
          <nav className="px-4 py-6 space-y-4">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`block py-2 text-base font-medium transition-colors ${
                  isActive(link.path)
                    ? 'text-teal-600'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {link.name}
              </Link>
            ))}
            <Link
              to="/contact"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center justify-center space-x-2 bg-teal-600 text-white px-6 py-3 rounded-full font-semibold w-full"
            >
              <Phone className="w-4 h-4" />
              <span>Free Case Review</span>
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
};

export default Header;
