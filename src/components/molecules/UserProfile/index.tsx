import React, { useContext } from 'react'
import { styled } from 'styled-components';
import { PiHandWaving } from "react-icons/pi";
import UserAvatar from '@/components/atoms/UserAvatar';
import { UserDataContext } from '@/context/UserDataContext';

const Container = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    width: 100%;
    gap: .5rem;

    div {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: .2rem;
        font-size: .8rem;
        color: ${({ theme }) => theme.colors.platinum};

        svg {
            height: 14px;
            width: 14px;
            color: yellow;
        }
    }
    
    span {
        font-size: .9rem;
        color: ${({ theme }) => theme.colors.white};
    }
`

export default function UserProfile() {
    const { user } = useContext(UserDataContext)
    console.log(user?.username)
  return (
    <>
        <UserAvatar $height={36} $width={36} />
        <Container>
            <div>Bem-vindo de volta <PiHandWaving/></div>
            <span>{user ? user.username : 'Carregando...'}</span>
        </Container>
    </>
  )
}

