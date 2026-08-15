export interface University {
  id: string;
  name: string;
  shortName: string;
  domain: string;
  logoUrl?: string;
}

export interface Department {
  id: string;
  universityId: string;
  name: string;
  code: string;
}

export interface Professor {
  id: string;
  departmentId: string;
  departmentName: string;
  name: string;
  title: string;
  avatarUrl?: string;
  avgTeaching: number;
  avgGrading: number;
  avgWorkload: number;
  overallRating: number;
  totalReviews: number;
  aiSummary?: string;
  tags: string[];
}

export interface Course {
  id: string;
  departmentId: string;
  departmentName: string;
  code: string;
  title: string;
  description: string;
  creditHours: number;
  avgRating: number;
  totalReviews: number;
  aiSummary?: string;
}

export interface CourseOffering {
  id: string;
  courseId: string;
  courseCode: string;
  courseTitle: string;
  professorId: string;
  professorName: string;
  semester: string;
}

export interface Review {
  id: string;
  offeringId: string;
  courseId: string;
  courseCode: string;
  courseTitle: string;
  professorId: string;
  professorName: string;
  ratingTeaching: number;
  ratingGrading: number;
  ratingWorkload: number;
  overallScore: number;
  comment: string;
  gradeReceived?: string;
  semesterTaken: string;
  helpfulCount: number;
  isHelpfulVoted?: boolean;
  createdAt: string;
  tags?: string[];
}

export interface SearchResultItem {
  id: string;
  type: 'professor' | 'course';
  title: string;
  subtitle: string;
  department: string;
  rating: number;
  reviewCount: number;
  url: string;
}
