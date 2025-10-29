import { Link } from 'react-router-dom';
import { Shield, Mail } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-slate-900 text-slate-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <span className="text-lg font-bold text-white">Military Disability Nexus</span>
            </div>
            <p className="text-sm text-slate-400 mb-4 max-w-md">
              Professional medical documentation services for veterans. Expert care and comprehensive support.
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-teal-500" />
                <span>contact@militarydisabilitynexus.com</span>
              </div>

            </div>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-white font-semibold mb-4">Services</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/services/nexus-rebuttal-letters" className="hover:text-teal-400 transition-colors">
                  Nexus Letters
                </Link>
              </li>
              <li>
                <Link to="/services/public-dbqs" className="hover:text-teal-400 transition-colors">
                  DBQs
                </Link>
              </li>
              <li>
                <Link to="/services/aid-attendance" className="hover:text-teal-400 transition-colors">
                  Aid & Attendance
                </Link>
              </li>
              <li>
                <Link to="/aid-attendance-form" className="hover:text-teal-400 transition-colors">
                  A&A Form
                </Link>
              </li>
              <li>
                <Link to="/services/cp-coaching" className="hover:text-teal-400 transition-colors">
                  C&P Coaching
                </Link>
              </li>
              <li>
                <Link to="/services/1151-claim" className="hover:text-teal-400 transition-colors">
                  1151 Claims
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-semibold mb-4">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/blog" className="hover:text-teal-400 transition-colors">
                  Blog
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-teal-400 transition-colors">
                  About
                </Link>
              </li>
              <li>
                <Link to="/contact" className="hover:text-teal-400 transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-slate-800 pt-8 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0 text-sm">
          <p className="text-slate-500">
            © {currentYear} Dr. Kishan Bhalani. All rights reserved.
          </p>
          <div className="flex space-x-6">
            <Link to="/blog" className="text-slate-500 hover:text-teal-400 transition-colors">
              Blog
            </Link>
            <Link to="/contact" className="text-slate-500 hover:text-teal-400 transition-colors">
              Contact
            </Link>
            <a href="#" className="text-slate-500 hover:text-teal-400 transition-colors">
              Privacy
            </a>
            <a href="#" className="text-slate-500 hover:text-teal-400 transition-colors">
              Terms
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
