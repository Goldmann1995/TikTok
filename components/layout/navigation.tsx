import { HStack, Icon } from '@chakra-ui/react'
import { useDisclosure, useUpdateEffect } from '@chakra-ui/react'
import { useScrollSpy } from 'hooks/use-scrollspy'
import { useRouter, usePathname} from 'next/navigation'
import * as React from 'react'

import { MobileNavButton } from '#components/mobile-nav'
import { MobileNavContent } from '#components/mobile-nav'
import { NavLink } from '#components/nav-link'
import siteConfig from '#data/config'

import ThemeToggle from './theme-toggle'
import { Button } from '@chakra-ui/react'
import { Link } from '@chakra-ui/react'
import { FiLogOut } from 'react-icons/fi'

interface NavigationProps {
  user: any;
  onSignOut: () => void;
}

const Navigation = ({ user, onSignOut }: NavigationProps) => {
  const mobileNav = useDisclosure()
  const router = useRouter()
  const path = usePathname()
  const activeId = useScrollSpy(
    siteConfig.header.links
      .filter(({ id }) => id)
      .map(({ id }) => `[id="${id}"]`),
    {
      threshold: 0.75,
    },
  )

  const mobileNavBtnRef = React.useRef<HTMLButtonElement>()

  useUpdateEffect(() => {
    mobileNavBtnRef.current?.focus()
  }, [mobileNav.isOpen])

  return (
    <HStack spacing="8">
      {siteConfig.header.links
        .filter(link => {
          if (user) {
            return !['login', 'signup'].includes(link.id || '');
          }
          return true;
        })
        .map(({ href, id, ...props }, i) => {
          return (
            <NavLink
              display={['none', null, 'block']}
              href={`/${user?.id}${href}` || `#${id}`}
              key={i}
              isActive={
                !!(
                  (id && activeId === id) ||
                  (href && !!path?.match(new RegExp(href)))
                )
              }
              {...props}
            >
              {props.label}
            </NavLink>
          )
        })}

      {user && (
        <HStack spacing={4}>
          <Button
            display={['none', null, 'block']}
            variant="ghost"
            onClick={onSignOut}
            rightIcon={<Icon as={FiLogOut} />}
          >
            {user.email}
          </Button>
        </HStack>
      )}

      <ThemeToggle />

      <MobileNavButton
        ref={mobileNavBtnRef}
        aria-label="Open Menu"
        onClick={mobileNav.onOpen}
      />

      <MobileNavContent isOpen={mobileNav.isOpen} onClose={mobileNav.onClose} />
    </HStack>
  )
}

export default Navigation
