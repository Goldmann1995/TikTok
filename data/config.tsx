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
        label: '我的资料',
        href: '/my',
        id: 'my',
        requireAuth: true
      },
      {
        label: '基础信息',
        href: '/fortune',
        id: 'fortune'
      },
      {
        label: '八字排盘',
        href: '/report',
        id: 'report'
      },
      {
        label: '命理解析',
        href: '/analysis',
        id: 'analysis'
      },
      {
        label: 'Login',
        href: '/login',
        id: 'login',
      },
      {
        label: 'Sign Up',
        href: '/signup',
        variant: 'primary',
        id: 'signup',
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
        title: '精准分析',
        description: '基于传统八字命理，科学解读您的命运轨迹，全面洞察您的优势与瓶颈。',
      },
      {
        icon: FiCheck,
        title: '个性化定制',
        description: '每一份命理分析都根据您的出生信息量身定制，独一无二，完全符合您的个体需求。',
      },
      {
        icon: FiCheck,
        title: '专业团队',
        description: '我们拥有经验丰富的命理师团队，深谙八字学与命理学，确保为您提供高质量的服务。',
      },

      {
        icon: FiCheck,
        title: '全方位解析',
        description: '从事业到健康，从婚姻到财运，我们帮助您预测未来，规避风险。',
      },
      {
        icon: FiCheck,
        title: '简便易用',
        description: '只需输入您的出生信息，便可快速获得专业排盘与分析报告，轻松了解自己的命运走向。',
      },      
      {
        icon: FiCheck,
        title: '尊重隐私',
        description: '您的个人信息我们严格保密，安全无忧。',
      },
    ],
  },
}

export default siteConfig
