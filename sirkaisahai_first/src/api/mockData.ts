import type { University, Department, Professor, Course, CourseOffering, Review } from '../types';

export const mockUniversity: University = {
  id: 'uni-superior',
  name: 'Superior University',
  shortName: 'Superior',
  domain: 'superior.edu.pk',
  logoUrl: 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=100&auto=format&fit=crop&q=80'
};

export const mockDepartments: Department[] = [
  { id: 'dept-cs', universityId: 'uni-superior', name: 'Computer Science', code: 'CS' },
  { id: 'dept-se', universityId: 'uni-superior', name: 'Software Engineering', code: 'SE' },
  { id: 'dept-cys', universityId: 'uni-superior', name: 'Cyber Security', code: 'CYS' },
  { id: 'dept-ds', universityId: 'uni-superior', name: 'Data Science', code: 'DS' },
  { id: 'dept-ai', universityId: 'uni-superior', name: 'Artificial Intelligence', code: 'AI' },
  { id: 'dept-it', universityId: 'uni-superior', name: 'Information Technology', code: 'IT' },
  { id: 'dept-iot', universityId: 'uni-superior', name: 'Internet of Things', code: 'IoT' }
];

export const mockProfessors: Professor[] = [];

export const mockCourses: Course[] = [
  {
    id: 'course-1',
    departmentId: 'dept-cs',
    departmentName: 'Computer Science',
    code: 'CS-201',
    title: 'Data Structures & Algorithms',
    description: 'Arrays, linked lists, trees, graphs, sorting, searching, time complexity analysis, and problem-solving techniques.',
    creditHours: 4,
    avgRating: 4.6,
    totalReviews: 0,
    aiSummary: 'A crucial core CS course.'
  },
  {
    id: 'course-2',
    departmentId: 'dept-cs',
    departmentName: 'Computer Science',
    code: 'CS-305',
    title: 'Database Management Systems',
    description: 'Relational model, SQL, normalization, indexing, transaction processing, and hands-on semester project.',
    creditHours: 4,
    avgRating: 4.5,
    totalReviews: 16,
    aiSummary: 'Highly practical course. The term project accounts for a large portion of the grade. SQL queries form the core of exams.'
  },
  {
    id: 'course-3',
    departmentId: 'dept-se',
    departmentName: 'Software Engineering',
    code: 'SE-310',
    title: 'Web Application Development',
    description: 'Frontend frameworks, REST APIs, asynchronous programming, database integration, and modern deployment pipelines.',
    creditHours: 3,
    avgRating: 4.8,
    totalReviews: 19,
    aiSummary: 'Top choice elective for SE/CS students. Great hands-on skills learned. Evaluation relies heavily on final group project presentation.'
  },
  {
    id: 'course-4',
    departmentId: 'dept-ba',
    departmentName: 'Business Administration',
    code: 'MGT-101',
    title: 'Principles of Management',
    description: 'Organizational behavior, leadership styles, strategic planning, decision making, and corporate ethics.',
    creditHours: 3,
    avgRating: 3.7,
    totalReviews: 12,
    aiSummary: 'Theory-based course requiring good memorization and case analysis. Quiz performance heavily dictates final letter grades.'
  },
  {
    id: 'course-5',
    departmentId: 'dept-math',
    departmentName: 'Mathematics & Science',
    code: 'MT-102',
    title: 'Calculus & Analytical Geometry',
    description: 'Limits, derivatives, integration techniques, multivariable calculus basics, and engineering applications.',
    creditHours: 3,
    avgRating: 4.1,
    totalReviews: 15,
    aiSummary: 'Standard freshman math course. Solved tutorial sheets are the best study material for midterms and finals.'
  }
];

export const mockOfferings: CourseOffering[] = [];

export const mockReviews: Review[] = [];
