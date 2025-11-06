import React, { useCallback } from 'react'
import { Card, Col, Row, Typography, Button, Tag } from 'antd'
import { ShoppingCartOutlined, HeartOutlined } from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography
const { Meta } = Card

interface HomeProduct {
  id: number
  name: string
  price: number
  category: string
  description: string
  image: string
}

const mockProducts: ReadonlyArray<HomeProduct> = [
  {
    id: 1,
    name: 'Laptop HP Pavilion',
    price: 899.99,
    category: 'Electronics',
    description: 'High performance laptop perfect for work and entertainment',
    image: 'https://via.placeholder.com/300x200/1890ff/white?text=Laptop'
  },
  {
    id: 2,
    name: 'iPhone 15 Pro',
    price: 999.99,
    category: 'Electronics', 
    description: 'Latest iPhone model with advanced camera system',
    image: 'https://via.placeholder.com/300x200/52c41a/white?text=iPhone'
  },
  {
    id: 3,
    name: 'Coffee Maker Deluxe',
    price: 159.99,
    category: 'Home',
    description: 'Premium coffee maker for the perfect morning brew',
    image: 'https://via.placeholder.com/300x200/f5222d/white?text=Coffee'
  },
  {
    id: 4,
    name: 'Running Shoes Pro',
    price: 129.99,
    category: 'Sports',
    description: 'Comfortable running shoes for professional athletes',
    image: 'https://via.placeholder.com/300x200/722ed1/white?text=Shoes'
  },
  {
    id: 5,
    name: 'Wireless Headphones',
    price: 79.99,
    category: 'Electronics',
    description: 'Premium sound quality with noise cancellation',
    image: 'https://via.placeholder.com/300x200/fa8c16/white?text=Headphones'
  },
  {
    id: 6,
    name: 'Smart Watch',
    price: 249.99,
    category: 'Electronics',
    description: 'Track your fitness and stay connected',
    image: 'https://via.placeholder.com/300x200/13c2c2/white?text=Watch'
  }
]

function formatCurrency(amount: number, locale: string = 'en-US', currency: string = 'USD'): string {
  return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount)
}

const HomePage: React.FC = () => {
  const handleAddToCart = useCallback((productId: number): void => {
    console.log('Add to cart:', productId)
  }, [])

  const handleAddToWishlist = useCallback((productId: number): void => {
    console.log('Add to wishlist:', productId)
  }, [])

  return (
    <div>
      <div style={{ 
        background: 'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)', 
        padding: '60px 0',
        borderRadius: '8px',
        marginBottom: '40px',
        color: 'white',
        textAlign: 'center'
      }}>
        <Title level={1} style={{ color: 'white', margin: 0 }}>
          Welcome to E-commerce Evolution
        </Title>
        <Paragraph style={{ fontSize: '18px', color: 'white', margin: '16px 0' }}>
          This is the base project that will evolve into a full-featured e-commerce platform
        </Paragraph>
        <Text style={{ color: 'white', opacity: 0.9 }}>
          🚀 Day 2: We'll connect these products with the real API
        </Text>
      </div>

      <Title level={2} style={{ marginBottom: '24px' }}>
        Featured Products
      </Title>
      
      <Row gutter={[24, 24]}>
        {mockProducts.map((product) => (
          <Col key={product.id} xs={24} sm={12} md={8} lg={6}>
            <Card
              hoverable
              style={{ height: '100%' }}
              cover={
                <div style={{ height: '200px', overflow: 'hidden' }}>
                  <img
                    alt={product.name}
                    src={product.image}
                    style={{ 
                      width: '100%', 
                      height: '100%', 
                      objectFit: 'cover' 
                    }}
                  />
                </div>
              }
              actions={[
                <Button 
                  key="cart"
                  type="primary"
                  icon={<ShoppingCartOutlined />}
                  onClick={() => handleAddToCart(product.id)}
                  size="small"
                >
                  Add to Cart
                </Button>,
                <Button
                  key="wishlist"
                  icon={<HeartOutlined />}
                  onClick={() => handleAddToWishlist(product.id)}
                  size="small"
                >
                  Wishlist
                </Button>
              ]}
            >
              <Meta
                title={
                  <div>
                    <div style={{ marginBottom: '8px' }}>
                      {product.name}
                    </div>
                    <Tag color="blue">{product.category}</Tag>
                  </div>
                }
                description={
                  <div>
                    <Paragraph 
                      ellipsis={{ rows: 2 }} 
                      style={{ margin: '8px 0', color: '#666' }}
                    >
                      {product.description}
                    </Paragraph>
                    <Title level={4} style={{ margin: 0, color: '#1890ff' }}>
                      {formatCurrency(product.price)}
                    </Title>
                  </div>
                }
              />
            </Card>
          </Col>
        ))}
      </Row>

      <div style={{ 
        marginTop: '60px', 
        padding: '40px',
        background: 'white',
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <Title level={3}>Project Evolution Timeline</Title>
        <Row gutter={[24, 16]} style={{ marginTop: '32px' }}>
          <Col span={6}>
            <Tag color="processing" style={{ padding: '8px 16px', fontSize: '14px' }}>
              Day 1: Clean Architecture (Backend)
            </Tag>
          </Col>
          <Col span={6}>
            <Tag color="default" style={{ padding: '8px 16px', fontSize: '14px' }}>
              Day 2: Products Feature (Frontend)
            </Tag>
          </Col>
          <Col span={6}>
            <Tag color="default" style={{ padding: '8px 16px', fontSize: '14px' }}>
              Day 3: Orders & Cart
            </Tag>
          </Col>
          <Col span={6}>
            <Tag color="default" style={{ padding: '8px 16px', fontSize: '14px' }}>
              Day 4: Authentication
            </Tag>
          </Col>
        </Row>
      </div>
    </div>
  )
}

export default HomePage





