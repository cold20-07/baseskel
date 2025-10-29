import { Award, Target, Users, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const About = () => {
  return (
    <div className="bg-slate-50 min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-teal-600 to-emerald-600 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">Who We Are</h1>
          <p className="text-xl text-teal-50">
            Professional medical documentation services
          </p>
        </div>
      </section>

      {/* Mission Statement */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-8 md:p-12 shadow-lg text-center">
            <h2 className="text-3xl font-bold text-slate-900 mb-6">
              Military Disability Nexus - Medical Documentation Expert
            </h2>
            <p className="text-lg text-slate-700 leading-relaxed mb-6">
              Military Disability Nexus provides professional medical documentation services for veterans. With extensive experience in medical-legal documentation, we focus on accurate, ethical, and comprehensive medical evidence.
            </p>
            <p className="text-lg text-slate-700 leading-relaxed">
              Every nexus letter, DBQ, and consultation is tailored to your specific case, grounded in clinical merit, and designed to provide clear, professional medical documentation for your needs.
            </p>
          </div>
        </div>
      </section>

      {/* Values Grid */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-900 mb-12 text-center">Our Values</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white rounded-2xl p-8 border-2 border-slate-200">
              <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-teal-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Mission</h3>
              <p className="text-slate-700">
                Precise evidence that stands on clinical merit and helps the adjudicator understand your case.
              </p>
            </div>

            <div className="bg-white rounded-2xl p-8 border-2 border-slate-200">
              <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center mb-4">
                <CheckCircle className="w-6 h-6 text-teal-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Values</h3>
              <p className="text-slate-700">
                Compassion • Accuracy • Transparency • Collaboration
              </p>
            </div>

            <div className="bg-white rounded-2xl p-8 border-2 border-slate-200">
              <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center mb-4">
                <Award className="w-6 h-6 text-teal-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Credentials</h3>
              <p className="text-slate-700">
                MD/DO/NP team • Multi-state licensure • Peer review QA
              </p>
            </div>


          </div>
        </div>
      </section>

      {/* Approach */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-900 mb-12 text-center">Our Approach</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-teal-100 rounded-2xl p-6 mb-4">
                <h3 className="text-xl font-bold text-slate-900 mb-3">Thorough Intake & Records</h3>
                <p className="text-slate-700">
                  We request only what's clinically relevant, then build a clean timeline.
                </p>
              </div>
            </div>

            <div className="text-center">
              <div className="bg-teal-100 rounded-2xl p-6 mb-4">
                <h3 className="text-xl font-bold text-slate-900 mb-3">Evidence-Based Rationale</h3>
                <p className="text-slate-700">
                  Differentials, risk factors, literature context when appropriate.
                </p>
              </div>
            </div>

            <div className="text-center">
              <div className="bg-teal-100 rounded-2xl p-6 mb-4">
                <h3 className="text-xl font-bold text-slate-900 mb-3">Quality Assurance</h3>
                <p className="text-slate-700">
                  Internal peer review for clarity, consistency, and defensibility.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-900 mb-8 text-center">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {[
              {
                q: 'Do you coordinate with attorneys/VSOs?',
                a: 'Yes. We are independent clinicians and can collaborate with your accredited representatives or attorneys upon request.',
              },
              {
                q: 'Who writes the opinions?',
                a: 'Board-certified physicians or experienced nurse practitioners with relevant specialty training.',
              },
              {
                q: 'What records do you need?',
                a: 'Service treatment records, VA medical records, and relevant private records. We guide you on specifics during intake.',
              },
              {
                q: 'How long does it take?',
                a: 'Most nexus letters: 7-10 business days. DBQs: 5-7 days. Rush service available for 36-48 hours delivery.',
              },
            ].map((faq, idx) => (
              <details key={idx} className="bg-white rounded-xl p-6 group border-2 border-slate-200">
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

      {/* CTA */}
      <section className="py-16 bg-gradient-to-br from-teal-600 to-emerald-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to get started?
          </h2>
          <p className="text-xl text-teal-50 mb-8">
            Contact us for a free case review
          </p>
          <Link
            to="/contact"
            data-testid="about-cta-button"
            className="inline-block bg-white text-teal-600 px-8 py-4 rounded-full font-semibold hover:bg-slate-50 transition-all hover:shadow-xl transform hover:-translate-y-1"
          >
            Get Free Consultation
          </Link>
        </div>
      </section>
    </div>
  );
};

export default About;
