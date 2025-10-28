import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Clock, Calendar, User } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const BlogPost = () => {
  const { slug } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await axios.get(`${API}/blog/${slug}`);
        setPost(response.data);
      } catch (error) {
        console.error('Error fetching post:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchPost();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600" />
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Post not found</h2>
          <Link to="/blog" className="text-teal-600 hover:text-teal-700">
            Back to Blog
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-50 min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-teal-600 to-emerald-600 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <Link
            to="/blog"
            className="inline-flex items-center space-x-2 text-teal-50 hover:text-white mb-6 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Blog</span>
          </Link>
          <div className="inline-block bg-teal-500 text-white px-4 py-2 rounded-full text-sm font-semibold mb-4">
            {post.category}
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">{post.title}</h1>
          <div className="flex flex-wrap items-center gap-6 text-teal-50">
            <div className="flex items-center space-x-2">
              <User className="w-5 h-5" />
              <span>{post.authorName}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Calendar className="w-5 h-5" />
              <span>{post.publishedAt}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-5 h-5" />
              <span>{post.readTime}</span>
            </div>
          </div>
        </div>
      </section>

      {/* Content */}
      <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-2xl p-8 md:p-12 shadow-lg">
          <div
            className="prose prose-slate prose-lg max-w-none"
            dangerouslySetInnerHTML={{ __html: post.contentHTML }}
          />
        </div>

        {/* Tags */}
        {post.tags && post.tags.length > 0 && (
          <div className="mt-8 flex flex-wrap gap-2">
            {post.tags.map((tag, idx) => (
              <span
                key={idx}
                className="bg-slate-200 text-slate-700 px-4 py-2 rounded-full text-sm font-medium"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* CTA */}
        <div className="mt-12 bg-gradient-to-br from-teal-600 to-emerald-600 rounded-2xl p-8 text-center">
          <h3 className="text-2xl font-bold text-white mb-4">
            Need help with your VA claim?
          </h3>
          <p className="text-teal-50 mb-6">
            Get expert guidance and documentation from our licensed clinicians
          </p>
          <Link
            to="/contact"
            className="inline-block bg-white text-teal-600 px-8 py-3 rounded-full font-semibold hover:bg-slate-50 transition-colors"
          >
            Get Free Consultation
          </Link>
        </div>
      </article>
    </div>
  );
};

export default BlogPost;
