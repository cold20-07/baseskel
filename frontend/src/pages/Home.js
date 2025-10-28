import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle, Award, Clock, Shield } from 'lucide-react';
import { useEffect, useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [services, setServices] = useState([]);
  const [blogPosts, setBlogPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [servicesRes, blogRes] = await Promise.all([
          axios.get(`${API}/services`),
          axios.get(`${API}/blog?limit=3`),
        ]);
        setServices(servicesRes.data.slice(0, 4));
        setBlogPosts(blogRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getIconComponent = (iconName) => {
    const icons = {
      'file-text': Shield,
      'clipboard': Award,
      'heart-pulse': CheckCircle,
      'users': Award,
      'lightbulb': Award,
      'file-search': Shield,
      'alert-triangle': CheckCircle,
    };
    return icons[iconName] || Shield;
  };

  return (
    <div className="bg-gradient-to-b from-white to-slate-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-50 via-emerald-50 to-slate-50 opacity-60" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 relative">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center space-x-2 bg-teal-100 text-teal-700 px-4 py-2 rounded-full text-sm font-semibold mb-6">
              <Award className="w-4 h-4" />
              <span>Professional Medical Documentation</span>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-900 mb-6 leading-tight">
              Expert Medical Documentation for <span className="text-teal-600">Veterans</span>
            </h1>
            <p className="text-lg sm:text-xl text-slate-600 mb-8 leading-relaxed max-w-2xl mx-auto">
              Professional medical evidence services by Dr. Kishan Bhalani. Comprehensive nexus letters, DBQs, and expert medical consultations for veterans.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/services"
                data-testid="hero-services-button"
                className="inline-flex items-center space-x-2 bg-teal-600 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-teal-700 transition-all hover:shadow-xl hover:shadow-teal-600/30 transform hover:-translate-y-1"
              >
                <span>Explore Services</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/contact"
                data-testid="hero-contact-button"
                className="inline-flex items-center space-x-2 bg-white text-slate-900 px-8 py-4 rounded-full font-semibold text-lg border-2 border-slate-200 hover:border-slate-300 transition-all hover:shadow-lg transform hover:-translate-y-1"
              >
                <span>Free Case Review</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Badges */}
      <section className="bg-white border-y border-slate-200 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="space-y-2">
              <div className="text-4xl font-bold text-teal-600">10,000+</div>
              <div className="text-slate-600">Veterans Served</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-teal-600">7-10 Days</div>
              <div className="text-slate-600">Average Turnaround</div>
            </div>
            <div className="space-y-2">
              <div className="text-4xl font-bold text-teal-600">98%</div>
              <div className="text-slate-600">Satisfaction Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">Our Services</h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Professional medical documentation and expert guidance for your VA disability claim
            </p>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto" />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {services.map((service) => {
                const IconComponent = getIconComponent(service.icon);
                return (
                  <Link
                    key={service.id}
                    to={`/services/${service.slug}`}
                    data-testid={`service-card-${service.slug}`}
                    className="group bg-white rounded-2xl p-6 border-2 border-slate-200 hover:border-teal-500 hover:shadow-xl transition-all transform hover:-translate-y-1"
                  >
                    <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center mb-4 group-hover:bg-teal-600 transition-colors">
                      <IconComponent className="w-6 h-6 text-teal-600 group-hover:text-white transition-colors" />
                    </div>
                    <h3 className="text-xl font-bold text-slate-900 mb-2">{service.title}</h3>
                    <p className="text-slate-600 mb-4 text-sm">{service.shortDescription}</p>
                    <div className="flex items-center text-teal-600 font-semibold text-sm group-hover:translate-x-1 transition-transform">
                      <span>Learn more</span>
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </div>
                  </Link>
                );
              })}
            </div>
          )}

          <div className="text-center mt-10">
            <Link
              to="/services"
              className="inline-flex items-center space-x-2 text-teal-600 font-semibold hover:text-teal-700 transition-colors"
            >
              <span>View All Services</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">How It Works</h2>
            <p className="text-lg text-slate-600">Simple, straightforward process</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
            {[
              { step: '01', title: 'Choose Service', desc: 'Select the service that fits your needs' },
              { step: '02', title: 'Submit Records', desc: 'Upload your medical and service records' },
              { step: '03', title: 'Expert Review', desc: 'Licensed clinicians review your case' },
              { step: '04', title: 'Telehealth', desc: 'Connect with our medical professionals remotely' },
              { step: '05', title: 'Receive Documentation', desc: 'Get your completed nexus letter or DBQ' },
            ].map((item, idx) => (
              <div key={idx} className="relative text-center">
                <div className="text-6xl font-bold text-teal-100 mb-4">{item.step}</div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">{item.title}</h3>
                <p className="text-slate-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Blog Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">Latest Resources</h2>
            <p className="text-lg text-slate-600">Guides and updates to help with your claim</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {blogPosts.map((post) => (
              <Link
                key={post.id}
                to={`/blog/${post.slug}`}
                data-testid={`blog-card-${post.slug}`}
                className="group bg-white rounded-2xl overflow-hidden border-2 border-slate-200 hover:border-teal-500 hover:shadow-xl transition-all transform hover:-translate-y-1"
              >
                <div className="h-48 bg-gradient-to-br from-teal-400 to-emerald-500" />
                <div className="p-6">
                  <div className="text-xs text-teal-600 font-semibold mb-2 uppercase">{post.category}</div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2 group-hover:text-teal-600 transition-colors">
                    {post.title}
                  </h3>
                  <p className="text-slate-600 text-sm mb-4">{post.excerpt}</p>
                  <div className="flex items-center justify-between text-sm text-slate-500">
                    <span>{post.publishedAt}</span>
                    <span>{post.readTime}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          <div className="text-center mt-10">
            <Link
              to="/blog"
              className="inline-flex items-center space-x-2 text-teal-600 font-semibold hover:text-teal-700 transition-colors"
            >
              <span>View All Articles</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-gradient-to-br from-teal-600 to-emerald-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to strengthen your VA claim?
          </h2>
          <p className="text-xl text-teal-50 mb-8">
            Get started with a free case review from our experienced team
          </p>
          <Link
            to="/contact"
            data-testid="cta-contact-button"
            className="inline-flex items-center space-x-2 bg-white text-teal-600 px-8 py-4 rounded-full font-semibold text-lg hover:bg-slate-50 transition-all hover:shadow-xl transform hover:-translate-y-1"
          >
            <span>Get Free Case Review</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
