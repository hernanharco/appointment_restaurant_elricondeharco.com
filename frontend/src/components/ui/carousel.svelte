<script lang="ts" context="module">
  // Definimos el contexto para que los subcomponentes (Item, Next, Prev) puedan acceder a la API
  import { getContext, setContext } from 'svelte';
  import { writable, type Writable } from 'svelte/store';

  export interface CarouselContext {
    api: Writable<any>;
    orientation: Writable<"horizontal" | "vertical">;
    canScrollPrev: Writable<boolean>;
    canScrollNext: Writable<boolean>;
    scrollPrev: () => void;
    scrollNext: () => void;
  }
</script>

<script lang="ts">
  import { cn } from "../../lib/utils";
  import emblaCarousel from 'embla-carousel-svelte';
  import { ArrowLeft, ArrowRight } from "lucide-svelte";
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  // PROPS
  export let orientation: "horizontal" | "vertical" = "horizontal";
  export let opts: any = {};
  export let plugins: any[] = [];
  export let className: string = "";

  // ESTADOS (Stores para que los hijos reaccionen)
  let emblaApi: any;
  const apiStore = writable(null);
  const orientationStore = writable(orientation);
  const canScrollPrev = writable(false);
  const canScrollNext = writable(false);

  $: orientationStore.set(orientation);

  function scrollPrev() { emblaApi?.scrollPrev(); }
  function scrollNext() { emblaApi?.scrollNext(); }

  function onSelect() {
    if (!emblaApi) return;
    canScrollPrev.set(emblaApi.canScrollPrev());
    canScrollNext.set(emblaApi.canScrollNext());
  }

  function onInit(event: CustomEvent) {
    emblaApi = event.detail;
    apiStore.set(emblaApi);
    if (emblaApi) {
      emblaApi.on("select", onSelect);
      emblaApi.on("reInit", onSelect);
      onSelect();
      dispatch('init', emblaApi);
    }
  }

  // Proveer contexto a los hijos
  setContext('carousel', {
    api: apiStore,
    orientation: orientationStore,
    canScrollPrev,
    canScrollNext,
    scrollPrev,
    scrollNext
  });

  // Manejo de teclado
  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      scrollPrev();
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      scrollNext();
    }
  }
</script>

<div
  class={cn("relative", className)}
  role="region"
  aria-roledescription="carousel"
  tabindex="-1"
>
  <div 
    class="overflow-hidden" 
    use:emblaCarousel={{ 
      options: { ...opts, axis: orientation === "horizontal" ? "x" : "y" }, 
      plugins 
    }}
    on:emblaInit={onInit}
  >
    <div class={cn(
      "flex",
      orientation === "horizontal" ? "-ml-4" : "-mt-4 flex-col",
      className
    )}>
      <slot />
    </div>
  </div>
  
  <slot name="buttons" />
</div>