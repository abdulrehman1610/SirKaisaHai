import type { Professor, Course, Review, Department, SearchResultItem } from '../types';
import {
  mockProfessors,
  mockCourses,
  mockReviews,
  mockDepartments,
  mockOfferings,
  mockUniversity
} from './mockData';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

// Helper for safe fetch with fallback to local mock data if server isn't running yet
async function fetchWithFallback<T>(url: string, options?: RequestInit, fallbackData?: T): Promise<T> {
  const fetchOptions: RequestInit = {
    ...options,
    credentials: 'include' // SEND COOKIES
  };
  try {
    const res = await fetch(url, fetchOptions);
    if (!res.ok) {
      throw new Error(`HTTP error ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    if (fallbackData !== undefined) {
      return fallbackData;
    }
    throw err;
  }
}

export const api = {
  // Get University metadata
  getUniversity() {
    return Promise.resolve(mockUniversity);
  },

  // Get list of departments
  async getDepartments(): Promise<Department[]> {
    return fetchWithFallback<Department[]>(`${API_BASE}/departments`, undefined, mockDepartments);
  },

  // Search across professors
  async search(query: string, departmentId?: string): Promise<SearchResultItem[]> {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (departmentId && departmentId !== 'all') params.append('departmentId', departmentId);

    const fallbackResults: SearchResultItem[] = [];
    const q = query.trim().toLowerCase();
    let profs = mockProfessors;
    if (departmentId && departmentId !== 'all') {
      profs = profs.filter((p) => p.departmentId === departmentId);
    }
    profs.forEach((p) => {
      if (!q || p.name.toLowerCase().includes(q) || p.departmentName.toLowerCase().includes(q)) {
        fallbackResults.push({
          id: p.id,
          type: 'professor',
          title: p.name,
          subtitle: p.title,
          department: p.departmentName,
          rating: p.overallRating,
          reviewCount: p.totalReviews,
          url: `/professor/${p.id}`
        });
      }
    });

    return fetchWithFallback<SearchResultItem[]>(
      `${API_BASE}/professors/search/all?${params.toString()}`,
      undefined,
      fallbackResults
    );
  },

  // Get Professor details by ID
  async getProfessorById(id: string): Promise<Professor | undefined> {
    const fallback = mockProfessors.find((p) => p.id === id);
    return fetchWithFallback<Professor>(`${API_BASE}/professors/${id}`, undefined, fallback);
  },

  // Add a new Teacher/Professor
  async addProfessor(data: { name: string; departmentId: string; title?: string; tags?: string[]; userEmail?: string }): Promise<Professor> {
    const res = await fetch(`${API_BASE}/professors`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include', // SEND COOKIES
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || 'Failed to add professor');
    }
    return await res.json();
  },

  // Get Course details by ID
  async getCourseById(id: string): Promise<Course | undefined> {
    return mockCourses.find((c) => c.id === id);
  },

  // Get all recent reviews from database
  async getRecentReviews(): Promise<Review[]> {
    return fetchWithFallback<Review[]>(`${API_BASE}/reviews`, undefined, []);
  },

  // Get Reviews for Professor
  async getReviewsForProfessor(profId: string): Promise<Review[]> {
    return fetchWithFallback<Review[]>(`${API_BASE}/reviews?professorId=${profId}`, undefined, []);
  },

  // Get Reviews for Course
  async getReviewsForCourse(courseId: string): Promise<Review[]> {
    return fetchWithFallback<Review[]>(`${API_BASE}/reviews`, undefined, []);
  },

  // Get Offerings for Review dropdown
  async getOfferings(): Promise<{ id: string; label: string; courseId: string; professorId: string }[]> {
    const profs = await this.getProfessorsList();
    if (profs.length > 0) {
      return profs.map((p) => ({
        id: `off-${p.id}`,
        label: `${p.name} (${p.departmentName})`,
        courseId: 'course-1',
        professorId: p.id
      }));
    }
    return mockOfferings.map((o) => ({
      id: o.id,
      label: `${o.courseCode} - ${o.courseTitle} (${o.professorName})`,
      courseId: o.courseId,
      professorId: o.professorId
    }));
  },

  async getProfessorsList(): Promise<Professor[]> {
    return fetchWithFallback<Professor[]>(`${API_BASE}/professors`, undefined, mockProfessors);
  },

  // Submit new review for teacher
  async submitReview(data: Omit<Review, 'id' | 'createdAt' | 'helpfulCount' | 'overallScore'> & { userEmail?: string }): Promise<Review> {
    const res = await fetch(`${API_BASE}/reviews`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include', // SEND COOKIES
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || 'Failed to submit review');
    }
    return await res.json();
  },

  // Vote helpful
  async voteHelpful(reviewId: string): Promise<{ success: boolean; newCount: number }> {
    try {
      const res = await fetch(`${API_BASE}/reviews/${reviewId}/vote`, { 
        method: 'POST',
        credentials: 'include' // SEND COOKIES
      });
      if (res.ok) {
        return await res.json();
      }
    } catch (err) {
      // Fallback
    }
    const rev = mockReviews.find((r) => r.id === reviewId);
    if (rev) {
      rev.helpfulCount += 1;
      return { success: true, newCount: rev.helpfulCount };
    }
    return { success: false, newCount: 0 };
  },

  // Auth OTP
  async sendOTP(email: string): Promise<{ success: boolean; message: string }> {
    const res = await fetch(`${API_BASE}/auth/request-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include', // SEND COOKIES
      body: JSON.stringify({ email })
    });
    return await res.json();
  },

  async verifyOTP(email: string, code: string): Promise<{ success: boolean; message?: string; email?: string }> {
    const res = await fetch(`${API_BASE}/auth/verify-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include', // SEND COOKIES
      body: JSON.stringify({ email, code })
    });
    return await res.json();
  },

  // Session Checks
  async checkSession(): Promise<{ authenticated: boolean; userId?: string; emailHash?: string }> {
    try {
      const res = await fetch(`${API_BASE}/auth/me`, {
        method: 'GET',
        credentials: 'include'
      });
      if (!res.ok) return { authenticated: false };
      return await res.json();
    } catch {
      return { authenticated: false };
    }
  },

  async logout(): Promise<{ success: boolean }> {
    try {
      const res = await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      });
      return await res.json();
    } catch {
      return { success: false };
    }
  }
};
