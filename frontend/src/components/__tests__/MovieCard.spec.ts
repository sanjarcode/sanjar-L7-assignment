import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MovieCard from '../MovieCard.vue'

describe('MovieCard', () => {
  it('renders movie details properly', () => {
    const movie = {
      id: 1,
      title: 'Inception',
      release_year: 2010,
      genres: [{ id: 1, name: 'Sci-Fi' }],
      actors: [],
      director: { id: 1, name: 'Christopher Nolan' }
    }

    const wrapper = mount(MovieCard, {
      props: { movie },
      global: {
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>'
          }
        }
      }
    })

    expect(wrapper.text()).toContain('Inception')
    expect(wrapper.text()).toContain('2010')
    expect(wrapper.text()).toContain('Christopher Nolan')
    expect(wrapper.text()).toContain('Sci-Fi')
  })
})
