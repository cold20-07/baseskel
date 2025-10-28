import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Award, CheckCircle, Shield, ArrowRight } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Services = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await axios.get(`${API}/services`);
        setServices(response.data);
      } catch (error) {
        console.error('Error fetching services:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchServices();
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
    <div className="bg-slate-50 min-h-screen">
      {/* Header */}
      <section className="bg-gradient-to-br from-teal-600 to-emerald-600 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">Our Services</h1>
          <p className="text-xl text-teal-50 max-w-2xl mx-auto">
            Claimant-specific medical evidence. Ethical, accurate, veteran-centered.
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="text-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto" />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {services.map((service) => {
                const IconComponent = getIconComponent(service.icon);
                return (
                  <div
                    key={service.id}
                    data-testid={`service-${service.slug}`}
                    className="bg-white rounded-2xl overflow-hidden border-2 border-slate-200 hover:border-teal-500 hover:shadow-xl transition-all group"
                  >
                    <div className="p-8">
                      <div className="w-14 h-14 bg-teal-100 rounded-xl flex items-center justify-center mb-6 group-hover:bg-teal-600 transition-colors">
                        <IconComponent className="w-7 h-7 text-teal-600 group-hover:text-white transition-colors" />
                      </div>
                      <h3 className="text-2xl font-bold text-slate-900 mb-3">{service.title}</h3>
                      <p className="text-slate-600 mb-6">{service.shortDescription}</p>
                      
                      <div className="space-y-3 mb-6">
                        {service.features.map((feature, idx) => (
                          <div key={idx} className="flex items-start space-x-2">
                            <CheckCircle className="w-5 h-5 text-teal-600 mt-0.5 flex-shrink-0" />
                            <span className="text-sm text-slate-700">{feature}</span>
                          </div>
                        ))}
                      </div>

                      <div className="flex items-center justify-between pt-6 border-t border-slate-200">
                        <div>
                          <div className="text-2xl font-bold text-slate-900">
                            ₹{service.basePriceInINR.toLocaleString()}
                          </div>
                          <div className="text-sm text-slate-500">{service.duration}</div>
                        </div>
                        <Link
                          to={`/services/${service.slug}`}
                          data-testid={`view-service-${service.slug}`}
                          className="inline-flex items-center space-x-2 bg-teal-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-teal-700 transition-all hover:shadow-lg transform hover:-translate-y-0.5"
                        >
                          <span>View Details</span>
                          <ArrowRight className="w-4 h-4" />
                        </Link>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-900 mb-8 text-center">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {[
              {
                q: 'What is a nexus letter?',
                a: 'A nexus letter is a medical document that establishes the connection between your military service and your current disability.',
              },
              {
                q: 'Do you complete VA DBQs?',
                a: 'Yes, we complete public DBQs that are currently accepted by the VA for various conditions.',
              },
              {
                q: 'Do you guarantee outcomes?',
                a: 'While we provide high-quality medical evidence, we cannot guarantee VA claim approvals as final decisions rest with the VA.',
              },
              {
                q: 'Can you help with Aid & Attendance?',
                a: 'Yes, we provide complete physician evaluations and documentation for VA Form 21-2680.',
              },
            ].map((faq, idx) => (
              <details key={idx} className="bg-slate-50 rounded-xl p-6 group">
                <summary className="font-semibold text-slate-900 cursor-pointer list-none flex justify-between items-center">
                  <span>{faq.q}</span>
                  <span className="text-teal-600 group-open:rotate-180 transition-transform">▼</span>
                </summary>
                <p className="mt-4 text-slate-600">{faq.a}</p>
              </details>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Services;
