import type { University, Department, Professor, Course, CourseOffering, Review } from '../types';

export const mockUniversity: University = {
  id: 'uni-superior',
  name: 'Superior University',
  shortName: 'Superior',
  domain: 'superior.edu.pk'
};

export const mockDepartments: Department[] = [
  { id: 'dept-cs', universityId: 'uni-superior', name: 'Computer Science', code: 'CS' },
  { id: 'dept-se', universityId: 'uni-superior', name: 'Software Engineering', code: 'SE' },
  { id: 'dept-cys', universityId: 'uni-superior', name: 'Cyber Security', code: 'CYS' },
  { id: 'dept-ds', universityId: 'uni-superior', name: 'Data Science', code: 'DS' },
  { id: 'dept-ai', universityId: 'uni-superior', name: 'Artificial Intelligence', code: 'AI' },
  { id: 'dept-it', universityId: 'uni-superior', name: 'Information Technology', code: 'IT' },
  { id: 'dept-iot', universityId: 'uni-superior', name: 'Internet of Things', code: 'IoT' },
  { id: 'dept-gd', universityId: 'uni-superior', name: 'Game Design', code: 'GD' }
];

export const mockProfessors: Professor[] = [];

export const mockCourses: Course[] = [
  {
    id: 'course-1',
    departmentId: 'dept-cs',
    departmentName: 'Computer Science',
    code: 'CS-201',
    title: 'Data Structures & Algorithms',
    description:
      'Arrays, linked lists, trees, graphs, sorting, searching, time complexity analysis, and problem-solving techniques.',
    creditHours: 4,
    avgRating: 4.6,
    totalReviews: 0,
    aiSummary: 'Core foundational CS course focused on trees, graphs, sorting, and runtime analysis.'
  },
  {
    id: 'course-2',
    departmentId: 'dept-cs',
    departmentName: 'Computer Science',
    code: 'CS-305',
    title: 'Database Management Systems',
    description:
      'Relational model, SQL, normalization, indexing, transaction processing, and hands-on semester project.',
    creditHours: 4,
    avgRating: 4.5,
    totalReviews: 16,
    aiSummary:
      'Practical course where the semester project carries major weight and SQL queries form the core of exams.'
  },
  {
    id: 'course-3',
    departmentId: 'dept-se',
    departmentName: 'Software Engineering',
    code: 'SE-310',
    title: 'Web Application Development',
    description:
      'Frontend frameworks, REST APIs, asynchronous programming, database integration, and modern deployment pipelines.',
    creditHours: 3,
    avgRating: 4.8,
    totalReviews: 19,
    aiSummary:
      'Hands-on elective for SE and CS students. Evaluation centers on the final full-stack project presentation.'
  },
  {
    id: 'course-4',
    departmentId: 'dept-ba',
    departmentName: 'Business Administration',
    code: 'MGT-101',
    title: 'Principles of Management',
    description:
      'Organizational behavior, leadership styles, strategic planning, decision making, and corporate ethics.',
    creditHours: 3,
    avgRating: 3.7,
    totalReviews: 12,
    aiSummary:
      'Theory-focused course built around case studies and regular quizzes that heavily influence final grades.'
  },
  {
    id: 'course-5',
    departmentId: 'dept-math',
    departmentName: 'Mathematics & Science',
    code: 'MT-102',
    title: 'Calculus & Analytical Geometry',
    description:
      'Limits, derivatives, integration techniques, multivariable calculus basics, and engineering applications.',
    creditHours: 3,
    avgRating: 4.1,
    totalReviews: 15,
    aiSummary:
      'Standard freshman mathematics course. Tutorial sheets closely reflect midterm and final exam structure.'
  }
];

export const mockOfferings: CourseOffering[] = [];

export const mockReviews: Review[] = [];
