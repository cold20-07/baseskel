const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://cwjsyxxzdwphhlpppxau.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3anN5eHh6ZHdwaGhscHBweGF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MzA2MTUsImV4cCI6MjA3NzIwNjYxNX0.7qmRxFhZr_rHwKRp_YaD3HB4D30feclY3xNPipoJvr0';

const supabase = createClient(supabaseUrl, supabaseKey);

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json',
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: '',
    };
  }

  const path = event.path.replace('/.netlify/functions/api', '');
  
  try {
    // Health check
    if (path === '/health') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          status: 'healthy',
          timestamp: new Date().toISOString(),
        }),
      };
    }

    // Get all services
    if (path === '/services') {
      const { data, error } = await supabase
        .from('services')
        .select('*');
      
      if (error) throw error;
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(data),
      };
    }

    // Get service by slug
    if (path.startsWith('/services/')) {
      const slug = path.replace('/services/', '');
      const { data, error } = await supabase
        .from('services')
        .select('*')
        .eq('slug', slug)
        .single();
      
      if (error) throw error;
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(data),
      };
    }

    // Get blog posts
    if (path === '/blog') {
      const { data, error } = await supabase
        .from('blog_posts')
        .select('*');
      
      if (error) throw error;
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(data),
      };
    }

    // Get blog post by slug
    if (path.startsWith('/blog/')) {
      const slug = path.replace('/blog/', '');
      const { data, error } = await supabase
        .from('blog_posts')
        .select('*')
        .eq('slug', slug)
        .single();
      
      if (error) throw error;
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(data),
      };
    }

    // Contact form
    if (path === '/contact' && event.httpMethod === 'POST') {
      const body = JSON.parse(event.body);
      const contactData = {
        id: Math.random().toString(36).substr(2, 9),
        name: body.name,
        email: body.email,
        phone: body.phone || null,
        subject: body.subject,
        message: body.message,
        status: 'new',
        createdAt: new Date().toISOString(),
      };

      const { data, error } = await supabase
        .from('contacts')
        .insert([contactData])
        .select()
        .single();
      
      if (error) throw error;
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(data),
      };
    }

    // 404 for unknown paths
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ error: 'Not found' }),
    };

  } catch (error) {
    console.error('API Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message }),
    };
  }
};