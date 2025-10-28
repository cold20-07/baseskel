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

  // Mock services data as fallback
  const mockServices = {
    "nexus-rebuttal-letters": {
      id: "1",
      slug: "nexus-rebuttal-letters",
      title: "Nexus & Rebuttal Letters",
      shortDescription: "Comprehensive medical opinions for claims and appeals",
      fullDescription: "Professional nexus and rebuttal letters that establish clear connections between your military service and medical conditions, or challenge unfavorable VA decisions. Our expert medical opinions provide the crucial evidence needed for both initial claims and appeals processes.",
      features: [
        "Nexus opinion letters",
        "Rebuttal to VA denials", 
        "Direct/secondary/aggravation analysis",
        "Clear medical rationale"
      ],
      basePriceInINR: 4999,
      duration: "7-10 business days",
      category: "nexus-letter",
      icon: "file-text",
      faqs: [
        {
          question: "What's the difference between nexus and rebuttal letters?",
          answer: "Nexus letters establish the connection between military service and a condition for initial claims. Rebuttal letters challenge VA decisions by providing contrary medical evidence and opinions."
        },
        {
          question: "Can you help with both initial claims and appeals?",
          answer: "Yes, we provide nexus letters for initial claims and rebuttal letters to challenge unfavorable VA decisions in appeals."
        }
      ]
    },
    "public-dbqs": {
      id: "2",
      slug: "public-dbqs",
      title: "Public DBQs",
      shortDescription: "Standardized disability questionnaires for VA claims",
      fullDescription: "Disability Benefits Questionnaires (DBQs) are standardized medical examination forms used by the VA to evaluate disability claims. Our licensed physicians complete these forms based on current VA guidelines and your medical condition.",
      features: [
        "Latest public VA DBQs",
        "Objective findings",
        "Functional impact"
      ],
      basePriceInINR: 3999,
      duration: "5-7 business days",
      category: "dbq",
      icon: "clipboard",
      faqs: [
        {
          question: "Do you complete VA DBQs?",
          answer: "Yes, we complete public DBQs that are currently accepted by the VA for various conditions."
        }
      ]
    },
    "aid-attendance": {
      id: "3",
      slug: "aid-attendance",
      title: "Aid & Attendance (21-2680)",
      shortDescription: "Enhanced pension benefits for veterans needing assistance",
      fullDescription: "Aid and Attendance is a benefit available to veterans and surviving spouses who require the regular assistance of another person. We provide comprehensive physician evaluations to support your A&A benefit claim.",
      features: [
        "Physician evaluation",
        "ADL documentation", 
        "When clinically indicated"
      ],
      basePriceInINR: 5999,
      duration: "10-14 business days",
      category: "aid-attendance",
      icon: "heart-pulse",
      faqs: [
        {
          question: "Can you help with Aid & Attendance?",
          answer: "Yes, we provide complete physician evaluations and documentation for VA Form 21-2680."
        }
      ]
    },
    "cp-coaching": {
      id: "4",
      slug: "cp-coaching",
      title: "C&P Coaching",
      shortDescription: "Preparation for compensation and pension examinations",
      fullDescription: "Prepare for your C&P exam with expert coaching. We help you understand what to expect, how to accurately report your symptoms, and provide tips to ensure your disabilities are properly documented.",
      features: [
        "What to expect",
        "Accurate symptom reporting",
        "Logbooks & lay tips"
      ],
      basePriceInINR: 2499,
      duration: "Same day or next business day",
      category: "coaching",
      icon: "users",
      faqs: [
        {
          question: "What is C&P coaching?",
          answer: "C&P coaching prepares you for your Compensation and Pension exam, helping you understand the process and communicate your condition effectively."
        }
      ]
    },
    "expert-consultation": {
      id: "5",
      slug: "expert-consultation",
      title: "One-on-One Consultation with Expert",
      shortDescription: "Personal consultation to review your claim with medical expert",
      fullDescription: "Schedule a comprehensive one-on-one consultation with Dr. Kishan Bhalani to review your VA claim, discuss your medical conditions, and receive personalized guidance on strengthening your case. This direct consultation provides expert insights tailored to your specific situation.",
      features: [
        "Personal consultation with Dr. Bhalani",
        "Comprehensive claim review",
        "Medical condition assessment",
        "Personalized recommendations"
      ],
      basePriceInINR: 3499,
      duration: "1-hour consultation scheduled within 3-5 days",
      category: "consultation",
      icon: "users",
      faqs: [
        {
          question: "How does the consultation work?",
          answer: "You'll have a scheduled one-on-one video or phone consultation with Dr. Kishan Bhalani to discuss your claim, medical conditions, and receive personalized guidance."
        }
      ]
    },
    "record-review": {
      id: "6",
      slug: "record-review",
      title: "Record Review",
      shortDescription: "Professional analysis of your medical documentation",
      fullDescription: "Our medical professionals review your service and medical records to identify conditions eligible for VA compensation, build a comprehensive timeline, and prepare targeted questions for your providers.",
      features: [
        "Service/med records synthesis",
        "Timeline build",
        "Provider question set"
      ],
      basePriceInINR: 2999,
      duration: "5-7 business days",
      category: "review",
      icon: "file-search",
      faqs: [
        {
          question: "What records should I provide?",
          answer: "Please provide your service treatment records, VA medical records, and any private medical records related to your conditions."
        }
      ]
    },
    "1151-claim": {
      id: "7",
      slug: "1151-claim",
      title: "1151 Claim (VA Medical Malpractice)",
      shortDescription: "Expert medical opinions for VA medical negligence claims",
      fullDescription: "Specialized medical documentation for 38 U.S.C. § 1151 claims when veterans are injured or their conditions worsen due to VA medical care. Our expert analysis helps establish negligence and causation for these complex claims requiring higher burden of proof.",
      features: [
        "VA treatment record analysis",
        "Medical negligence assessment",
        "Causation nexus opinions",
        "Standard of care evaluation"
      ],
      basePriceInINR: 7999,
      duration: "10-14 business days",
      category: "malpractice",
      icon: "alert-triangle",
      faqs: [
        {
          question: "What is a 1151 claim?",
          answer: "A 1151 claim is filed when a veteran believes they were injured or their condition worsened due to VA medical care negligence, surgical errors, medication mistakes, or other treatment-related harm."
        },
        {
          question: "How is this different from a regular VA claim?",
          answer: "1151 claims require proving VA negligence and deviation from medical standards, not just service connection. They have a higher burden of proof but can provide compensation even for non-service-connected conditions."
        }
      ]
    }
  };

  useEffect(() => {
    const fetchService = async () => {
      try {
        const response = await axios.get(`${API}/services/${slug}`);
        setService(response.data);
      } catch (error) {
        console.error('Error fetching service:', error);
        // Fallback to mock data when backend is unavailable
        const mockService = mockServices[slug];
        if (mockService) {
          setService(mockService);
        }
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
