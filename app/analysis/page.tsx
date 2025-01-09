'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/app/store/userStore'
import { 
  Box, Container, Text, VStack, 
  useColorModeValue,
  Table, Thead, Tbody, Tr, Th, Td,
  Button,
  Icon
} from '@chakra-ui/react'
import ReactMarkdown from 'react-markdown'
import { FaFilePdf } from 'react-icons/fa'
import html2pdf from 'html2pdf.js'

export default function Analysis() {
  const router = useRouter()
  const analysisResult = useUserStore(state => state.analysisResult)
  const [displayText, setDisplayText] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isTypingComplete, setIsTypingComplete] = useState(false)

  useEffect(() => {
    if (!analysisResult) {
      router.push('/report')
      return
    }

    const sections = analysisResult?.data?.sections;


    // 确保 `sections` 存在且是数组
    if (Array.isArray(sections) && sections[1]?.[0]?.[1]) {
      const analysisText = sections[1][0][1]; // 获取正确的文本
      
      // 模拟打字机效果
      if (currentIndex < analysisText.length) {
        // 模拟打字逻辑
        const timer = setTimeout(() => {
          setDisplayText(prev => prev + analysisText[currentIndex])
          setCurrentIndex(prev => prev + 1)
        }, 50) // 调整速度
  
        return () => clearTimeout(timer)
      }
    } else {
      console.error("");
    }

    // 检查是否打字完成
    if (analysisText && currentIndex >= analysisText.length) {
      setIsTypingComplete(true)
    }
  }, [analysisResult, currentIndex, router])

  const bgGradient = useColorModeValue(
    'linear(to-br, pink.50, purple.50)',
    'linear(to-br, purple.900, blue.900)'
  )

  const handleSavePDF = () => {
    const contentElement = document.querySelector('.css-1fpgkyz p')
    if (!contentElement) {
      console.error('未找到内容元素')
      return
    }

    // 获取文本内容
    const textContent = contentElement.textContent || ''
    
    // 创建一个格式化的临时容器
    const tempContainer = document.createElement('div')
    tempContainer.style.padding = '20px'
    tempContainer.style.background = '#ffffff'
    tempContainer.style.color = '#000000'
    tempContainer.style.fontFamily = 'sans-serif'
    tempContainer.innerHTML = `
      <h1 style="text-align: center; margin-bottom: 20px; font-size: 24px; color: #000;">命理分析报告</h1>
      <div style="white-space: pre-wrap; line-height: 1.6; font-size: 16px;">
        ${textContent}
      </div>
    `

    const options = {
      margin: [10, 10],
      filename: '命理分析报告.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { 
        scale: 2,
        backgroundColor: '#ffffff'
      },
      jsPDF: { 
        unit: 'mm', 
        format: 'a4', 
        orientation: 'portrait'
      }
    }

    html2pdf()
      .from(tempContainer)
      .set(options)
      .save()
      .catch(err => {
        console.error('PDF生成失败:', err)
      });
  }

  return (
    <Box
      minH="100vh"
      bgGradient={bgGradient}
      position="relative"
      overflow="hidden"
    >
      {/* 背景装饰 */}
      <Box
        position="absolute"
        top={0}
        left={0}
        right={0}
        bottom={0}
        opacity={0.1}
        bgImage="url('/stars-pattern.png')"
        zIndex={0}
      />

      <Container 
        id="analysis-content"
        maxW="container.md" 
        py={20} 
        position="relative" 
        zIndex={1}
      >
        <VStack spacing={8}>
          <Text
            fontSize="3xl"
            fontWeight="bold"
            bgGradient="linear(to-r, pink.400, purple.400)"
            bgClip="text"
            opacity="0"
            animation="fadeIn 2s ease-in forwards"
            sx={{
              '@keyframes fadeIn': {
                '0%': { opacity: 0 },
                '100%': { opacity: 1 }
              }
            }}
          >
            命理解析
          </Text>

          <Box
            bg={useColorModeValue('whiteAlpha.900', 'whiteAlpha.100')}
            borderRadius="3xl"
            p={8}
            boxShadow="2xl"
            backdropFilter="blur(10px)"
            border="1px solid"
            borderColor={useColorModeValue('pink.100', 'whiteAlpha.200')}
            w="full"
            minH="60vh"
            position="relative"
            overflow="hidden"
          >
            <ReactMarkdown
              components={{
                p: (props) => (
                  <Text
                    mb={4}
                    color={useColorModeValue('gray.700', 'whiteAlpha.900')}
                    {...props}
                  />
                ),
                h1: (props) => (
                  <Text
                    fontSize="2xl"
                    fontWeight="bold"
                    mb={4}
                    bgGradient="linear(to-r, pink.400, purple.400)"
                    bgClip="text"
                    {...props}
                  />
                ),
                h2: (props) => (
                  <Text
                    fontSize="xl"
                    fontWeight="bold"
                    mb={3}
                    color={useColorModeValue('purple.500', 'purple.300')}
                    {...props}
                  />
                ),
                h3: (props) => (
                  <Text
                    fontSize="lg"
                    fontWeight="bold"
                    mb={2}
                    color={useColorModeValue('pink.500', 'pink.300')}
                    {...props}
                  />
                ),
                h4: (props) => (
                  <Text
                    fontSize="md"
                    fontWeight="bold"
                    mb={2}
                    color={useColorModeValue('purple.400', 'purple.200')}
                    {...props}
                  />
                ),
                ul: (props) => (
                  <Box as="ul" pl={4} mb={4} {...props} />
                ),
                li: (props) => (
                  <Text
                    as="li"
                    mb={2}
                    color={useColorModeValue('gray.700', 'whiteAlpha.900')}
                    {...props}
                  />
                ),
                table: (props) => (
                  <Table 
                    variant="simple" 
                    my={4} 
                    borderWidth="1px"
                    borderColor={useColorModeValue('pink.100', 'whiteAlpha.300')}
                    borderRadius="lg"
                    overflow="hidden"
                    {...props}
                  />
                ),
                thead: (props) => (
                  <Thead 
                    bg={useColorModeValue('pink.50', 'whiteAlpha.100')}
                    {...props}
                  />
                ),
                tbody: (props) => <Tbody {...props} />,
                tr: (props) => (
                  <Tr 
                    _hover={{
                      bg: useColorModeValue('pink.50', 'whiteAlpha.50')
                    }}
                    {...props}
                  />
                ),
                th: (props) => (
                  <Th 
                    py={3}
                    textAlign="center"
                    color={useColorModeValue('gray.600', 'whiteAlpha.900')}
                    fontWeight="bold"
                    fontSize="sm"
                    borderColor={useColorModeValue('pink.100', 'whiteAlpha.300')}
                    {...props}
                  />
                ),
                td: (props) => (
                  <Td 
                    py={3}
                    textAlign="center"
                    borderColor={useColorModeValue('pink.100', 'whiteAlpha.300')}
                    color={useColorModeValue('gray.700', 'whiteAlpha.900')}
                    fontSize="sm"
                    {...props}
                  />
                ),
              }}
            >
              {displayText}
            </ReactMarkdown>
          </Box>
        </VStack>
      </Container>

      {/* PDF 下载按钮 */}
      {isTypingComplete && (
        <Box
          position="fixed"
          bottom="2rem"
          right="2rem"
          zIndex={2}
        >
          <Button
            leftIcon={<Icon as={FaFilePdf} />}
            size="lg"
            bgGradient="linear(to-r, purple.500, pink.500)"
            color="white"
            _hover={{
              bgGradient: "linear(to-r, purple.600, pink.600)",
              transform: "scale(1.05)"
            }}
            _active={{
              bgGradient: "linear(to-r, purple.700, pink.700)",
            }}
            boxShadow="lg"
            onClick={handleSavePDF}
            borderRadius="full"
            px={6}
          >
            保存为PDF
          </Button>
        </Box>
      )}
    </Box>
  )
}