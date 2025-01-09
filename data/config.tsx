import { Button } from '@chakra-ui/react'
import { Link } from '@saas-ui/react'
import { NextSeoProps } from 'next-seo'
import { FaGithub, FaTwitter } from 'react-icons/fa'
import { FiCheck } from 'react-icons/fi'
import { Logo } from './logo'

const siteConfig = {
  logo: Logo,
  seo: {
    title: '未来说',
    description: '用生辰八字提供人生建议。',
  } as NextSeoProps,
  termsUrl: '#',
  privacyUrl: '#',
  header: {
    links: [
      {
        label: '首页',
        href: '/',
        id: 'home'
      },
      {
        label: '算命',
        href: '/fortune',
        id: 'fortune'
      },
      {
        label: 'Login',
        href: '/login',
      },
      {
        label: 'Sign Up',
        href: '/signup',
        variant: 'primary',
      },
    ],
  },
  footer: {
    copyright: (
      <>
        Copyright © {new Date().getFullYear()} Built by{' '}
        <Link href="mailto:einfach.goldmann@gmail.com">Goldmann AI Group</Link>
      </>
    ),
    links: [
      {
        href: '/BaZI.jpg',
        label: 'Contact',
      },
      // {
      //   href: 'https://twitter.com/saas_js',
      //   label: <FaTwitter size="14" />,
      // },
      {
        href: 'https://github.com/Goldmann1995',
        label: <FaGithub size="14" />,
      },
    ],
  },
  signup: {
    title: '开启你的未来说',
    features: [
      {
        icon: FiCheck,
        title: '生辰八字',
        description: '分析您的出生时间，揭示命运的基本结构。',
      },
      {
        icon: FiCheck,
        title: '流年大运',
        description: '根据每年的运势变化，为您提供详细的流年分析。',
      },
      {
        icon: FiCheck,
        title: '合冲刑害',
        description: '解析八字中的合冲刑害，帮助您理解人际关系和生活中的挑战。',
      },
      {
        icon: FiCheck,
        title: '六亲十神',
        description: '根据十神推测您的命运轨迹，揭示可能的机遇与风险。',
      },
    ],
  },
}

export default siteConfig
