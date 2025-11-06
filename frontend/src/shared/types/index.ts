// ====== SHARED TYPES (Domain & API contracts) ======

export type ISODateString = string
export type Slug = string

export type CurrencyCode = 'USD' | 'EUR' | 'ARS' | 'MXN' | 'BRL' | 'CLP'

export interface Money {
  amount: number
  currency: CurrencyCode
}

export interface ProductImage {
  url: string
  alt: string
  width?: number
  height?: number
}

export interface ProductVariant {
  id: number
  sku: string
  name?: string
  price: Money
  stock: number
  attributes?: Record<string, string>
}

export interface ProductDimensions {
  weightKg?: number
  widthCm?: number
  heightCm?: number
  lengthCm?: number
}

export interface Product {
  id: number
  sku: string
  name: string
  slug: Slug
  description?: string
  categories: string[]
  brand?: string
  images: ProductImage[]
  price: Money
  compareAtPrice?: Money
  stock: number
  rating?: number
  variants?: ProductVariant[]
  dimensions?: ProductDimensions
  isActive?: boolean
  createdAt?: ISODateString
  updatedAt?: ISODateString
}

export type UserRole = 'customer' | 'admin'

export interface UserAddress {
  id?: number
  fullName: string
  line1: string
  line2?: string
  city: string
  state?: string
  postalCode: string
  country: string
  phone?: string
  isDefault?: boolean
}

export interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  role: UserRole
  avatarUrl?: string
  phone?: string
  addresses?: UserAddress[]
  isActive?: boolean
  createdAt?: ISODateString
  updatedAt?: ISODateString
}

export interface OrderItem {
  id?: number
  productId: number
  variantId?: number
  sku: string
  name: string
  quantity: number
  unitPrice: Money
  totalPrice: Money
  imageUrl?: string
}

export type OrderStatus =
  | 'pending'
  | 'confirmed'
  | 'processing'
  | 'shipped'
  | 'delivered'
  | 'cancelled'

export type PaymentMethod = 'card' | 'paypal' | 'bank_transfer' | 'cash_on_delivery'
export type PaymentStatus = 'pending' | 'paid' | 'failed' | 'refunded'

export interface Order {
  id: number
  userId: number
  items: OrderItem[]
  subtotal: Money
  taxAmount: Money
  shippingAmount: Money
  discountAmount?: Money
  totalAmount: Money
  status: OrderStatus
  paymentMethod: PaymentMethod
  paymentStatus: PaymentStatus
  shippingAddress: UserAddress
  billingAddress?: UserAddress
  trackingNumber?: string
  notes?: string
  createdAt?: ISODateString
  updatedAt?: ISODateString
}

export interface CartItem {
  productId: number
  variantId?: number
  name: string
  price: Money
  quantity: number
  imageUrl?: string
  addedAt?: ISODateString
}

export interface Cart {
  items: CartItem[]
  subtotal: Money
  totalItems: number
}

export interface PaginationMeta {
  page: number
  limit: number
  totalItems: number
  totalPages: number
}

export interface ApiResponse<T> {
  data: T
  message?: string
  meta?: Record<string, unknown>
}

export interface PaginatedResponse<T> {
  data: T[]
  meta: PaginationMeta
}

export interface PaginationParams {
  page?: number
  limit?: number
  search?: string
  sort?: string
  order?: 'asc' | 'desc'
  filters?: Record<string, unknown>
}

export interface LoginRequest {
  email: string
  password: string
  rememberMe?: boolean
}

export interface RegisterRequest {
  email: string
  password: string
  firstName: string
  lastName: string
}

export interface AuthResponse {
  accessToken: string
  refreshToken?: string
  tokenType?: 'Bearer'
  expiresAt?: ISODateString
  user: User
}

export interface ApiError {
  message: string
  status: number
  errorCode?: string
  details?: unknown
  trackingId?: string
}