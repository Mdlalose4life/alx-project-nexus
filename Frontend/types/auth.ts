export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
  new_password_confirm: string;
}

export interface BusinessCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Business {
  id: number;
  name: string;
  slug: string;
  description?: string;
  category: BusinessCategory;
  owner: User;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  parent?: ProductCategory;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description?: string;
  category: ProductCategory;
  business: Business;
  price: string;
  stock_quantity: number;
  is_active: boolean;
  images?: ProductImage[];
  created_at: string;
  updated_at: string;
}

export interface ProductImage {
  id: number;
  image: string;
  alt_text?: string;
  is_primary: boolean;
}

export interface SearchParams {
  q?: string;
  category?: string;
  page?: number;
  limit?: number;
  min_price?: number;
  max_price?: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

