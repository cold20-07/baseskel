import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Clock, ArrowRight } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Blog = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  const categories = [
    { label: 'All', value: '' },
    { label: 'Nexus Letters', value: 'nexus-letters' },
    { label: 'Exam Prep', value: 'exam-prep' },
    { label: 'Aid & Attendance', value: 'aid-attendance' },
  ];

  useEffect(() => {
    fetchPosts();
  }, [selectedCategory, searchQuery]);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      let url = `${API}/blog?limit=20`;
      if (selectedCategory) url += `&category=${selectedCategory}`;
      if (searchQuery) url += `&q=${searchQuery}`;

      const response = await axios.get(url);
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchPosts();
  };

  return (
    <div className="bg-slate-50 min-h-screen">
      {/* Header */}
      <section className="bg-gradient-to-br from-teal-600 to-emerald-600 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center space-x-2 bg-teal-500 text-white px-4 py-2 rounded-full text-sm font-semibold mb-6">
            <span>BLOG</span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">Guides & Updates</h1>
          <p className="text-xl text-teal-50">
            Expert insights, tips, and resources for your VA disability claim
          </p>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Search and Filters */}
        <div className="mb-12">
          <form onSubmit={handleSearch} className="mb-6">
            <div className="relative max-w-xl mx-auto">
              <input
                type="text"
                placeholder="Search articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                data-testid="blog-search-input"
                className="w-full px-6 py-4 pl-12 rounded-full border-2 border-slate-200 focus:border-teal-500 focus:outline-none text-slate-900"
              />
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
            </div>
          </form>

          <div className="flex flex-wrap justify-center gap-3">
            {categories.map((cat) => (
              <button
                key={cat.value}
                onClick={() => setSelectedCategory(cat.value)}
                data-testid={`category-${cat.value || 'all'}`}
                className={`px-6 py-2 rounded-full font-medium transition-all ${
                  selectedCategory === cat.value
                    ? 'bg-teal-600 text-white shadow-lg'
                    : 'bg-white text-slate-700 hover:bg-slate-100 border-2 border-slate-200'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Posts Grid */}
        {loading ? (
          <div className="text-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600 mx-auto" />
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-xl text-slate-600">No articles found</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post) => (
              <Link
                key={post.id}
                to={`/blog/${post.slug}`}
                data-testid={`blog-post-${post.slug}`}
                className="group bg-white rounded-2xl overflow-hidden border-2 border-slate-200 hover:border-teal-500 hover:shadow-xl transition-all transform hover:-translate-y-1"
              >
                <div className="h-48 bg-gradient-to-br from-teal-400 to-emerald-500" />
                <div className="p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs text-teal-600 font-semibold uppercase">{post.category}</span>
                    <span className="text-xs text-slate-500">{post.publishedAt}</span>
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2 group-hover:text-teal-600 transition-colors">
                    {post.title}
                  </h3>
                  <p className="text-slate-600 text-sm mb-4">{post.excerpt}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2 text-sm text-slate-500">
                      <Clock className="w-4 h-4" />
                      <span>{post.readTime}</span>
                    </div>
                    <div className="flex items-center text-teal-600 font-semibold text-sm group-hover:translate-x-1 transition-transform">
                      <span>Read more</span>
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Blog;
