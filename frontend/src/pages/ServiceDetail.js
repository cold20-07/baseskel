import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, ArrowLeft, Clock, DollarSign } from 'lucide-react';
import axios from 'axios';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '../components/ui/accordion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ServiceDetail = () => {
  const { slug } = useParams();
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchService = async () => {
      try {
        const response = await axios.get(`${API}/services/${slug}`);
        setService(response.data);
      } catch (error) {
        console.error('Error fetching service:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchService();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600" />
      </div>
    );
  }

  if (!service) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Service not found</h2>
          <Link to="/services" className="text-teal-600 hover:text-teal-700">
            Back to Services
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-50 min-h-screen">
      {/* Header */}
      <section className="bg-gradient-to-br from-teal-600 to-emerald-600 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            to="/services"
            className="inline-flex items-center space-x-2 text-teal-50 hover:text-white mb-6 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Services</span>
          </Link>
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">{service.title}</h1>
          <p className="text-xl text-teal-50">{service.shortDescription}</p>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Overview */}
            <div className="bg-white rounded-2xl p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-4">Overview</h2>
              <p className="text-slate-700 leading-relaxed">{service.fullDescription}</p>
            </div>

            {/* What's Included */}
            <div className="bg-white rounded-2xl p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">What's Included</h2>
              <div className="space-y-4">
                {service.features.map((feature, idx) => (
                  <div key={idx} className="flex items-start space-x-3">
                    <CheckCircle className="w-6 h-6 text-teal-600 mt-0.5 flex-shrink-0" />
                    <span className="text-slate-700">{feature}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* FAQ */}
            <div className="bg-white rounded-2xl p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">Frequently Asked Questions</h2>
              <Accordion type="single" collapsible className="w-full">
                {service.faqs.map((faq, idx) => (
                  <AccordionItem key={idx} value={`item-${idx}`}>
                    <AccordionTrigger className="text-left">{faq.question}</AccordionTrigger>
                    <AccordionContent>
                      <p className="text-slate-600">{faq.answer}</p>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 bg-white rounded-2xl p-8 border-2 border-teal-500 shadow-xl">
              <div className="mb-6">
                <div className="text-sm text-slate-500 mb-2">Starting at</div>
                <div className="text-4xl font-bold text-slate-900 mb-1">
                  ₹{service.basePriceInINR.toLocaleString()}
                </div>
              </div>

              <div className="space-y-4 mb-6">
                <div className="flex items-center space-x-3 text-slate-700">
                  <Clock className="w-5 h-5 text-teal-600" />
                  <span>{service.duration}</span>
                </div>
                <div className="flex items-center space-x-3 text-slate-700">
                  <CheckCircle className="w-5 h-5 text-teal-600" />
                  <span>Licensed clinicians</span>
                </div>
              </div>

              <Link
                to="/contact"
                data-testid="book-now-button"
                className="w-full bg-teal-600 text-white px-6 py-4 rounded-full font-semibold text-center hover:bg-teal-700 transition-all hover:shadow-lg block"
              >
                Book Now
              </Link>

              <p className="text-sm text-slate-500 mt-4 text-center">
                Get a free consultation before booking
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceDetail;
