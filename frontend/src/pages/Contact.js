import { useState } from 'react';
import { Mail, Phone, Send, Upload, CheckCircle } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';
import FileUpload from '../components/FileUpload';
import FileList from '../components/FileList';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [contactId, setContactId] = useState(null);
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [fileRefreshTrigger, setFileRefreshTrigger] = useState(0);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API}/contact`, formData);
      setSubmitted(true);
      setContactId(response.data.id); // Store contact ID for file uploads
      setShowFileUpload(true);
      toast.success('Message sent successfully! You can now upload supporting documents.');
      setFormData({ name: '', email: '', phone: '', subject: '', message: '' });
    } catch (error) {
      console.error('Error submitting form:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle file upload completion
  const handleFileUploadComplete = (uploadedFile) => {
    toast.success(`File "${uploadedFile.original_filename}" uploaded successfully!`);
    setFileRefreshTrigger(prev => prev + 1); // Trigger file list refresh
  };

  // Handle file upload error
  const handleFileUploadError = (error) => {
    toast.error(`Upload failed: ${error}`);
  };

  return (
    <div className="bg-slate-50 min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-teal-600 to-emerald-600 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">Contact Us</h1>
          <p className="text-xl text-teal-50">
            Get in touch for a free case review or to ask questions
          </p>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Contact Info */}
          <div className="lg:col-span-1 space-y-8">
            <div>
              <h3 className="text-2xl font-bold text-slate-900 mb-6">Get in Touch</h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Mail className="w-5 h-5 text-teal-600" />
                  </div>
                  <div>
                    <div className="font-semibold text-slate-900">Email</div>
                    <div className="text-slate-600">contact@militarydisabilitynexus.com</div>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Phone className="w-5 h-5 text-teal-600" />
                  </div>
                  <div>
                    <div className="font-semibold text-slate-900">Phone</div>
                    <div className="text-slate-600">+91-XXXX-XXXXXX</div>
                  </div>
                </div>


              </div>
            </div>


          </div>

          {/* Contact Form */}
          <div className="lg:col-span-2">
            {submitted ? (
              <div className="space-y-8">
                <div className="bg-white rounded-2xl p-8 text-center shadow-lg">
                  <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <CheckCircle className="w-8 h-8 text-teal-600" />
                  </div>
                  <h3 className="text-2xl font-bold text-slate-900 mb-4">Message Sent!</h3>
                  <p className="text-slate-600 mb-6">
                    Thank you for reaching out. We'll review your message and get back to you within 24-48 hours.
                  </p>
                  
                  {showFileUpload && (
                    <div className="bg-teal-50 border border-teal-200 rounded-lg p-4 mb-6">
                      <div className="flex items-center justify-center space-x-2 text-teal-700 mb-2">
                        <Upload className="w-5 h-5" />
                        <span className="font-medium">Upload Supporting Documents</span>
                      </div>
                      <p className="text-sm text-teal-600">
                        You can now upload medical records, service records, or other supporting documents.
                      </p>
                    </div>
                  )}
                  
                  <button
                    onClick={() => {
                      setSubmitted(false);
                      setShowFileUpload(false);
                      setContactId(null);
                    }}
                    className="bg-teal-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-teal-700 transition-colors"
                  >
                    Send Another Message
                  </button>
                </div>

                {/* File Upload Section */}
                {showFileUpload && contactId && (
                  <div className="bg-white rounded-2xl p-8 shadow-lg">
                    <h4 className="text-xl font-bold text-slate-900 mb-6">Upload Documents</h4>
                    <FileUpload
                      contactId={contactId}
                      onUploadComplete={handleFileUploadComplete}
                      onUploadError={handleFileUploadError}
                      maxFiles={10}
                      acceptedTypes="image/*,.pdf,.doc,.docx,.txt"
                      maxSizeInMB={50}
                    />
                  </div>
                )}

                {/* File List Section */}
                {contactId && (
                  <div className="bg-white rounded-2xl p-8 shadow-lg">
                    <FileList 
                      contactId={contactId} 
                      refreshTrigger={fileRefreshTrigger}
                    />
                  </div>
                )}
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="bg-white rounded-2xl p-8 shadow-lg">
                <h3 className="text-2xl font-bold text-slate-900 mb-6">Send Us a Message</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">
                      Name *
                    </label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      data-testid="contact-name-input"
                      className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">
                      Email *
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      data-testid="contact-email-input"
                      className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-teal-500 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">
                      Phone
                    </label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      data-testid="contact-phone-input"
                      className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-teal-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-700 mb-2">
                      Subject *
                    </label>
                    <input
                      type="text"
                      name="subject"
                      value={formData.subject}
                      onChange={handleChange}
                      required
                      data-testid="contact-subject-input"
                      className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-teal-500 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="mb-6">
                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Message *
                  </label>
                  <textarea
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows="6"
                    data-testid="contact-message-input"
                    className="w-full px-4 py-3 border-2 border-slate-200 rounded-lg focus:border-teal-500 focus:outline-none resize-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  data-testid="contact-submit-button"
                  className="w-full bg-teal-600 text-white px-8 py-4 rounded-full font-semibold hover:bg-teal-700 transition-all hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                      <span>Sending...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      <span>Send Message</span>
                    </>
                  )}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
