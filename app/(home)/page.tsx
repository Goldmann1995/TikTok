'use client'

import { Container, Heading, Button, VStack, Text } from '@chakra-ui/react'
import { MotionBox } from '#components/motion/box'
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()

  const handleClick = () => {
    router.push('/fortune')
  }

  return (
    <Container
      maxW="container.xl"
      height="80vh"
      display="flex"
      alignItems="center"
      justifyContent="center"
      pt={0}
      pb={0}
    >
      <VStack spacing={6}>
        <MotionBox
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <VStack spacing={2}>
            <Heading
              fontSize={{ base: "4xl", md: "6xl" }}
              fontWeight="bold"
              textAlign="center"
              bgGradient="linear(to-r, #7928CA, #FF0080)"
              bgClip="text"
            >
              未来说里说未来，零丁洋里叹零丁
            </Heading>
            <Text
              fontSize={{ base: "md", md: "lg" }}
              color="gray.500"
              textAlign="center"
              maxW="md"
              px={4}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              基于八字命理的人生解析，为您提供事业、感情、财运等多维度分析。结果报告将以下一年的流月运势方式呈现。
            </Text>
          </VStack>
        </MotionBox>

        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Button
            size="lg"
            bgGradient="linear(to-r, #7928CA, #FF0080)"
            color="white"
            px={8}
            py={6}
            fontSize="lg"
            _hover={{
              bgGradient: "linear(to-r, #6017a9, #d6006b)",
              transform: "scale(1.05)"
            }}
            transition="all 0.2s"
            onClick={handleClick}
          >
            开始解密
          </Button>
        </MotionBox>
      </VStack>
    </Container>
  )
}