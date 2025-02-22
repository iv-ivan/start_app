import type { Route } from "./+types/home";
import { Main } from "../main/main";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Test frontend" },
    { name: "description", content: "SPA with single input field" },
  ];
}

export default function Home() {
  return <Main />;
}
