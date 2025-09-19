import { useState, useEffect } from "react";

const UseViewport = (threshold: number = 768) => {
  const [isAboveThreshold, setIsAboveThreshold] = useState<boolean>(false)

  useEffect(() => {
    if (typeof window !== "undefined") {
      const handleResize = () => {
        setIsAboveThreshold(window.innerWidth > threshold)
      };

      setIsAboveThreshold(window.innerWidth > threshold)

      window.addEventListener("resize", handleResize)

      return () => {
        window.removeEventListener("resize", handleResize)
      };
    }
  }, [threshold])

  return isAboveThreshold
}

export default UseViewport
