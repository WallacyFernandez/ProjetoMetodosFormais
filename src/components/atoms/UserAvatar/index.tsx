'use client'

import React from 'react'
import { styled } from 'styled-components'

interface UserAvatarProps {
  $height: number,
  $width: number
};

const AvatarImg = styled.img<UserAvatarProps>`
  height: ${({ $height }) => `${$height}px`};
  width: ${({ $width }) => `${$width}px`};
  border-radius: 50%;
`;

export default function UserAvatar({ $height, $width} : UserAvatarProps) {
  return <AvatarImg loading='lazy' $height={$height} $width={$width} src="/Avatar.svg" alt="Avatar" />
}